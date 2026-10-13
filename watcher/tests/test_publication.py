import json
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app import main, publication, sync
from app.database import Article, Base
from app.intake import intake_loose_files
from app.metadata import parse_metadata


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.posts = self.root / "posts"
        self.posts.mkdir()
        self.engine = create_engine(f"sqlite:///{self.root / 'test.db'}")
        self.addCleanup(self.engine.dispose)
        Base.metadata.create_all(self.engine)
        self.sessions = sessionmaker(bind=self.engine)
        self.now = datetime(2026, 10, 14, 15, 42, 31)
        for target, value in (
            ("app.sync.SessionLocal", self.sessions),
            ("app.main.SessionLocal", self.sessions),
            ("app.main.settings", replace(main.settings, posts_mount=str(self.posts))),
            ("app.sync.settings", replace(sync.settings, posts_mount=str(self.posts))),
            ("app.sync.local_now", lambda: self.now),
            ("app.publication.settings", replace(publication.settings, timezone="Asia/Shanghai")),
        ):
            patcher = patch(target, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def article_dir(self, name="20-01-01-example"):
        directory = self.posts / name
        directory.mkdir()
        (directory / "content.md").write_text("# Example\n", encoding="utf-8")
        return directory

    def article(self, article_id):
        with self.sessions() as session:
            return session.get(Article, article_id)

    def test_single_sync_uses_import_time_and_preserves_it_after_edits(self):
        directory = self.article_dir()
        article_id, _ = sync.sync_single(directory.name)
        self.assertEqual(self.article(article_id).published_at, self.now)
        self.assertNotEqual(self.article(article_id).created_at, datetime(2020, 1, 1))
        self.now = datetime(2026, 10, 15, 12, 0, 0)
        self.assertIsNone(sync.sync_single(directory.name))
        (directory / "content.md").write_text("# Edited\n", encoding="utf-8")
        sync.sync_single(directory.name)
        self.assertEqual(self.article(article_id).published_at, datetime(2026, 10, 14, 15, 42, 31))

    def test_full_sync_uses_import_time_and_keeps_existing_dates(self):
        self.article_dir()
        article_id, _ = sync.full_sync()[0]
        self.assertEqual(self.article(article_id).published_at, self.now)
        historical = datetime(2020, 1, 1)
        with self.sessions() as session:
            session.get(Article, article_id).published_at = historical
            session.commit()
        sync.full_sync()
        self.assertEqual(self.article(article_id).published_at, historical)

    def test_manual_timestamp_survives_intake(self):
        (self.posts / "Example.md").write_text(
            "published_at: 2021-12-31T18:30:45+08:00\nsummary: Example\ntags: demo\n\n# Body\n",
            encoding="utf-8",
        )
        name = intake_loose_files(self.posts)[0]
        self.assertTrue(name.startswith("21-12-31-"))
        meta = json.loads((self.posts / name / ".meta").read_text())
        self.assertEqual(meta["published_at"], "2021-12-31T18:30:45")
        self.assertEqual(meta["tags"], ["demo"])
        self.assertEqual((self.posts / name / "content.md").read_text(), "# Body\n")
        article_id, _ = sync.sync_single(name)
        self.assertEqual(self.article(article_id).published_at, datetime(2021, 12, 31, 18, 30, 45))

    def test_date_only_header_does_not_force_midnight(self):
        (self.posts / "Example.md").write_text("2020/01/01\n\n# Body\n", encoding="utf-8")
        name = intake_loose_files(self.posts)[0]
        self.assertTrue(name.startswith("20-01-01-"))
        article_id, _ = sync.sync_single(name)
        self.assertEqual(self.article(article_id).published_at, self.now)

    def test_offset_is_converted_to_site_time(self):
        self.assertEqual(
            publication.parse_publication_time("2026-12-31T18:30:00Z"),
            datetime(2027, 1, 1, 2, 30),
        )
        self.assertEqual(
            publication.parse_publication_time("2026/10/14 09:30"), datetime(2026, 10, 14, 9, 30),
        )

    def test_invalid_manual_time_leaves_source_for_correction(self):
        path = self.posts / "Example.md"
        path.write_text("published_at: 2026-10-14\n\n# Body\n", encoding="utf-8")
        self.assertEqual(intake_loose_files(self.posts), [])
        self.assertTrue(path.is_file())

    def test_invalid_directory_metadata_does_not_insert_article(self):
        directory = self.article_dir()
        (directory / ".meta").write_text('{"published_at": "invalid"}', encoding="utf-8")
        self.assertIsNone(sync.sync_single(directory.name))
        self.assertEqual(sync.full_sync(), [])
        with self.sessions() as session:
            self.assertEqual(session.execute(select(Article)).scalars().all(), [])

    def test_empty_publication_and_multiple_tags_reach_database(self):
        (self.posts / "Example.md").write_text(
            "summary: Example summary\ntags: Python, Docker，随笔、Python; Linux；Docker\n"
            "published_at: \n\n# Body\n", encoding="utf-8",
        )
        name = intake_loose_files(self.posts)[0]
        article_id, title = sync.sync_single(name)
        main._process_new_article(article_id, title)
        article = self.article(article_id)
        self.assertEqual(article.summary, "Example summary")
        self.assertEqual({tag.name for tag in article.tags}, {"Python", "Docker", "随笔", "Linux"})
        self.assertEqual(article.published_at, self.now)
        self.assertEqual((self.posts / name / "content.md").read_text(), "# Body\n")

    def test_directory_header_is_supported_and_omitted_fields_are_preserved(self):
        directory = self.article_dir()
        path = directory / "content.md"
        path.write_text("summary: First\ntags: Python\npublished_at:\n\n# Body\n")
        article_id, title = sync.sync_single(directory.name)
        main._process_new_article(article_id, title)
        (directory / ".meta").unlink()
        path.write_text("summary: Changed\n\n# Edited\n")
        sync.sync_single(directory.name)
        main._process_new_article(article_id, title)
        article = self.article(article_id)
        self.assertEqual(article.summary, "Changed")
        self.assertEqual([tag.name for tag in article.tags], ["Python"])
        self.assertEqual(article.published_at, self.now)

    def test_explicit_empty_summary_and_tags_clear_fields(self):
        directory = self.article_dir()
        article_id, title = sync.sync_single(directory.name)
        sync.update_article_meta(article_id, "Summary", ["Python"])
        (directory / "content.md").write_text("summary:\ntags:\npublished_at:\n\n# Body\n")
        main._process_new_article(article_id, title)
        article = self.article(article_id)
        self.assertEqual(article.summary, "")
        self.assertEqual(article.tags, [])
        self.assertEqual(article.published_at, self.now)

    def test_legacy_fields_and_body_examples_are_not_metadata(self):
        content = "简介：正文\ntag：Python\nsummary: Still body text\n"
        cleaned, meta = parse_metadata(content)
        self.assertEqual(cleaned, content)
        self.assertEqual(meta, {})
        content = "# Body\n\nsummary: Example\ntags: Example\n"
        self.assertEqual(parse_metadata(content), (content, {}))

    def test_empty_publication_in_meta_uses_import_time(self):
        directory = self.article_dir()
        (directory / ".meta").write_text('{"published_at": "", "summary": "Summary"}')
        article_id, _ = sync.sync_single(directory.name)
        self.assertEqual(self.article(article_id).published_at, self.now)


if __name__ == "__main__":
    unittest.main()

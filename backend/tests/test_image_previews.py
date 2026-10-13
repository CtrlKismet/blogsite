from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from PIL import Image

from app.config import settings
from app.database import get_session
from app.routers import images
from app.services.image_service import get_preview_path, guess_media_type


@pytest.fixture
def source(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "IMAGE_CACHE_DIR", str(tmp_path / "cache"))
    path = tmp_path / "photo.png"
    Image.effect_noise((1800, 1200), 60).convert("RGB").save(path)
    return path


def test_preview_is_smaller_and_reused(source):
    original = source.read_bytes()
    preview = get_preview_path(source, 640)
    assert preview != source
    assert preview.stat().st_size < len(original)
    with Image.open(preview) as image:
        assert image.format == "WEBP"
        assert image.size == (640, 427)
    stamp = preview.stat().st_mtime_ns
    assert get_preview_path(source, 640) == preview
    assert preview.stat().st_mtime_ns == stamp
    assert source.read_bytes() == original


def test_source_update_invalidates_preview(source):
    first = get_preview_path(source, 640)
    Image.effect_noise((1600, 1000), 40).convert("RGB").save(source)
    assert get_preview_path(source, 640) != first


def test_animated_webp_is_preserved(source):
    animation = source.with_suffix(".webp")
    frames = [Image.new("RGB", (50, 50), color) for color in ("red", "blue")]
    frames[0].save(animation, save_all=True, append_images=frames[1:], duration=100, loop=0)
    assert get_preview_path(animation, 640) == animation


def test_transparency_is_preserved(source):
    with Image.open(source) as image:
        image = image.convert("RGBA")
        image.putalpha(100)
        image.save(source)
    preview = get_preview_path(source, 640)
    assert preview != source
    with Image.open(preview) as image:
        assert image.mode == "RGBA"
        assert image.getpixel((0, 0))[3] == 100


def test_invalid_image_falls_back(source):
    source.write_bytes(b"invalid image")
    assert get_preview_path(source, 640) == source


def test_modern_image_types_without_system_mime_database(monkeypatch):
    monkeypatch.setattr("app.services.image_service.mimetypes.guess_type", lambda _: (None, None))
    assert guess_media_type("preview.webp") == "image/webp"
    assert guess_media_type("photo.AVIF") == "image/avif"


def test_larger_preview_falls_back(source):
    source = source.with_suffix(".webp")
    Image.new("RGB", (1, 1), "white").save(source, lossless=True)
    assert get_preview_path(source, 640) == source
    assert not list(Path(settings.IMAGE_CACHE_DIR).glob("*.webp"))


def test_image_endpoint(source, monkeypatch):
    app = FastAPI()
    app.include_router(images.router)
    app.dependency_overrides[get_session] = lambda: None
    monkeypatch.setattr(images, "get_image_path", AsyncMock(return_value=source))
    with TestClient(app) as client:
        preview = client.get("/images/1/photo.png?w=640")
        assert preview.status_code == 200
        assert preview.headers["content-type"] == "image/webp"
        assert preview.headers["cache-control"] == "public, max-age=3600"
        original = client.get("/images/1/photo.png")
        assert original.content == source.read_bytes()
        assert original.headers["content-type"] == "image/png"
        assert client.get("/images/1/photo.png?w=99999").status_code == 422

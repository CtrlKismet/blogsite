// <auto-generated />
using System;
using BlogSite.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;

namespace BlogSite.Migrations
{
    [DbContext(typeof(BlogDbContext))]
    [Migration("20181217135016_addTag")]
    partial class addTag
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "2.1.4-rtm-31024")
                .HasAnnotation("Relational:MaxIdentifierLength", 64);

            modelBuilder.Entity("BlogSite.Models.Article", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd();

                    b.Property<string>("content");

                    b.Property<string>("ellipsisContent");

                    b.Property<DateTime>("lastModifyTime");

                    b.Property<string>("tagId");

                    b.Property<string>("title");

                    b.HasKey("id");

                    b.ToTable("article");
                });

            modelBuilder.Entity("BlogSite.Models.Tag", b =>
                {
                    b.Property<int>("id")
                        .ValueGeneratedOnAdd();

                    b.Property<string>("tagName");

                    b.HasKey("id");

                    b.ToTable("tag");
                });
#pragma warning restore 612, 618
        }
    }
}

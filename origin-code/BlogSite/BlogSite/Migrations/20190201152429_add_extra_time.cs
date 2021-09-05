using System;
using Microsoft.EntityFrameworkCore.Migrations;

namespace BlogSite.Migrations
{
    public partial class add_extra_time : Migration
    {
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<DateTime>(
                name: "addTime",
                table: "article",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));
        }

        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "addTime",
                table: "article");
        }
    }
}

using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using BlogSite.Models;
using Newtonsoft.Json.Linq;
using BlogSite.Data;
using Microsoft.AspNetCore.Cors;
using Microsoft.EntityFrameworkCore;

namespace BlogSite.Controllers
{
    public class HomeController : Controller
    {
        private readonly BlogDbContext _context;

        public HomeController(BlogDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            return View();
        }

        public IActionResult About()
        {
            return View(0);
        }

        public IActionResult Archive()
        {
            return View();
        }

        public IActionResult BlogDetail(int? ID)
        {
            if (!ID.HasValue) RedirectToAction("Index");
            return View(ID.Value);
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}

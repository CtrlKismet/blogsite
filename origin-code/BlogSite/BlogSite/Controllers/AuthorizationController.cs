using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using BlogSite.Data;
using BlogSite.Models;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json.Linq;

namespace BlogSite.Controllers
{
    [Authorize]
    public class AuthorizationController : Controller
    {
        private readonly BlogDbContext _context;

        public AuthorizationController(BlogDbContext context)
        {
            _context = context;
        }

        public IActionResult NewBlog()
        {
            return View();
        }

        public IActionResult Management(int ID)
        {
            return View("NewBlog", ID);
        }

        [AllowAnonymous]
        public IActionResult Login()
        {
            return View();
        }

        [AllowAnonymous]
        [HttpPost]
        public async Task<IActionResult> Login(User user)
        {
            if (user.name == "ctrlkismet" && user.pwd == "hyz981029")
            {
                var claims = new List<Claim> { new Claim(ClaimTypes.Name, user.name) };
                var claimIdentity = new ClaimsIdentity(claims, CookieAuthenticationDefaults.AuthenticationScheme);
                ClaimsPrincipal _user = new ClaimsPrincipal(claimIdentity);
                await HttpContext.SignInAsync(CookieAuthenticationDefaults.AuthenticationScheme, _user);
            }
            return RedirectToAction("Index", "Home");
        }

        [AllowAnonymous]
        public async Task<IActionResult> LogOut()
        {
            await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
            return RedirectToAction("Index","Home");
        }
    }

    public class User
    {
        public string name { get; set; }
        public string pwd { get; set; }
    }
}
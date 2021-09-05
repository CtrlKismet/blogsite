using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using BlogSite.Data;
using BlogSite.Models;
using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json.Linq;

namespace BlogSite.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TagController : ControllerBase
    {
        private readonly BlogDbContext _context;

        public TagController(BlogDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        [EnableCors("any")]
        public JArray Get()
        {
            JArray jArray = new JArray();
            //List<string> s = new List<string>();
            foreach (var tg in _context.tag)
            {
                JObject jObject = new JObject
                {
                    ["id"] = tg.id,
                    ["name"] = tg.tagName
                };
                jArray.Add(jObject);
                //s.Add(tg.tagName);
            }
            //按名称排序
            //s = s.OrderBy(x => x).ToList();
            //JArray newjArray = new JArray();
            //foreach (var name in s)
            //{
            //    newjArray.Add(jArray.FirstOrDefault(x => x["name"].ToString() == name));
            //}
            //return newjArray;
            return jArray;
        }

        [HttpGet("{id}")]
        [EnableCors("any")]
        public string[] Get(int id)
        {
            string[] tagsId;
            try
            {
                tagsId = _context.article.FirstOrDefault(x => x.id == id).tagId.Split(";");
            }
            catch (Exception e)
            {
                throw e;
            }
            JArray jArray = new JArray();
            string[] tagsName = new string[tagsId.Length - 1];
            for (int i = 0; i < tagsId.Length - 1; i++)
            {
                tagsName[i] = _context.tag.FirstOrDefault(x => x.id == Convert.ToInt32(tagsId[i])).tagName;
            }
            return tagsName;
        }
    }

}
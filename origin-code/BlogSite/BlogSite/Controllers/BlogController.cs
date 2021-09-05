using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json.Linq;
using BlogSite.Data;
using BlogSite.Models;
using Newtonsoft.Json;

namespace BlogSite.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class BlogController : ControllerBase
    {
        private readonly BlogDbContext _context;

        public BlogController(BlogDbContext context)
        {
            _context = context;
        }

        public bool JudgeIfContinue(string selectedTagID, int selectedBlogID, string tagId, int id)
        {
            if (selectedBlogID == 0 && id == 0) return false;
            if ((selectedTagID != "0" && !tagId.Contains(selectedTagID)) || id == 0) return true; //有标签被选中
            if (selectedBlogID != -1 && id != selectedBlogID) return true; //有博客被选中
            return false;
        }

        public string[] returnParameter = { "id", "title", "ellipsisContent", "content", "addTime", "lastModifyTime" };

        public JObject RemoveUseless(JObject jObject, string needReturn)
        {
            for (int i = 0; i < needReturn.Length; i++)
            {
                if (needReturn[i] == '0')
                {
                    jObject.Remove(returnParameter[i]);
                }
            }
            return jObject;
        }

        [HttpGet]
        [EnableCors("any")]
        public JArray Get(string jsonFilter)
        {
            ArticleFilter filter = JsonConvert.DeserializeObject<ArticleFilter>(jsonFilter);

            string selectedTagID = filter.tagId != null ? filter.tagId : "0";
            int selectedBlogID = filter.id != -1 ? filter.id : -1;


            JArray jArray = new JArray();
            foreach (var art in _context.article)
            {
                if (JudgeIfContinue(selectedTagID, selectedBlogID, art.tagId, art.id)) continue;

                JObject jObject = new JObject
                {
                    ["id"] = art.id,
                    ["title"] = art.title,
                    ["ellipsisContent"] = art.ellipsisContent,
                    ["content"] = art.content,
                    ["addTime"] = art.addTime,
                    ["lastModifyTime"] = art.lastModifyTime
                };
                jObject = RemoveUseless(jObject, filter.needReturn);
                jArray.Add(jObject);
            }
            var obj = jArray.Last;
            JArray newJarray = new JArray();
            while (obj != jArray.First)
            {
                newJarray.Add(obj);
                obj = obj.Previous;
            }
            newJarray.Add(jArray.First);
            return newJarray;
        }

        [HttpGet("{id}")]
        [EnableCors("any")]
        public string[] Get(int id)
        {
            Article preArticle = _context.article.FirstOrDefault(x => x.id == id - 1);
            Article nextArticle = _context.article.FirstOrDefault(x => x.id == id + 1);
            return new string[] { preArticle == null || id == 1 ? "" : preArticle.title, nextArticle == null ? "" : nextArticle.title };
        }

        [HttpPost]
        [EnableCors("any")]
        public bool Post([FromBody]Article article)
        {
            try
            {
                if (article.id == -1) article.id = 0;
                article.addTime = DateTime.Now;
                article.lastModifyTime = DateTime.Now;
                _context.article.Add(article);
                _context.SaveChanges();
            }
            catch (Exception e)
            {
                if (e != null) return false;
                throw e;
            }
            return true;
        }

        [HttpPut]
        [EnableCors("any")]
        public bool Put([FromBody]Article article)
        {
            try
            {
                Article preArticle = _context.article.FirstOrDefault(x => x.id == article.id);
                if (preArticle == null) return false;
                preArticle.lastModifyTime = DateTime.Now;
                preArticle.tagId = article.tagId;
                preArticle.title = article.title;
                preArticle.ellipsisContent = article.ellipsisContent;
                preArticle.content = article.content;
                _context.SaveChanges();
            }
            catch (Exception e)
            {
                if (e != null) return false;
                throw e;
            }
            return true;

        }
    }

    public class ArticleFilter : Article
    {
        public string needReturn { get; set; }
    }
}
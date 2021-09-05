using System;
using System.Collections.Generic;
using System.IO;
using System.Web;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Cors;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http.Internal;
using static System.Net.Mime.MediaTypeNames;

namespace BlogSite.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ImageController : ControllerBase
    {
        private readonly Dictionary<string, string> contentTypDict = new Dictionary<string, string> {
            {"jpg","image/jpeg"},
            {"jpeg","image/jpeg"},
            {"jpe","image/jpeg"},
            {"png","image/png"},
            {"gif","image/gif"},
            {"ico","image/x-ico"},
            {"tif","image/tiff"},
            {"tiff","image/tiff"},
            {"fax","image/fax"},
            {"wbmp","image//vnd.wap.wbmp"},
            {"rp","image/vnd.rn-realpix"}
        };

        [HttpGet("{fileName}")]
        [EnableCors("any")]
        public IActionResult Get(string fileName)
        {
            if (string.IsNullOrEmpty(fileName))
            {
                return NotFound();
            }
            string filePath = "../home/img/" + fileName;
            var imgType = fileName.Split(".")[1].ToLower();
            var contentTypeStr = contentTypDict[imgType];
            using (var stream = new FileStream(filePath, FileMode.Open))
            {
                var bytes = new byte[stream.Length];
                stream.Read(bytes, 0, bytes.Length);
                stream.Close();
                return new FileContentResult(bytes, contentTypeStr);
            }

            //memoryStream.Seek(0, SeekOrigin.Begin);

            //Response.Headers.Add("Content-Disposition", "attachment; filename=" + fileName);
            //return new FileContentResult(memoryStream,"image/jpeg");//文件流方式，指定文件流对应的ContenType。
        }

        [HttpPost]
        [Consumes("application/json", "multipart/form-data")]
        [EnableCors("any")]
        public async Task<string> PostAsync(IFormCollection files)
        {
            if (files.Files.Count == 0) return null;
            IFormFile file = files.Files[0];
            if (file == null || file.Length == 0) return null;
            string fileType = file.ContentType.Split('/')[0], fileExt = file.ContentType.Split('/')[1];

            //文件格式错误
            if (fileType != "image") return null;

            string fileName= Guid.NewGuid().ToString() + "." + fileExt;
            string filePath = "../home/img/" + fileName;

            using (var stream = new FileStream(filePath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }
            return fileName;
        }
    }
}
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace BlogSite.Models
{
    public class Article
    {
        public int id { get; set; }
        public string title { get; set; }
        public string ellipsisContent { get; set; }
        public string content { get; set; }
        public DateTime addTime { get; set; }
        public DateTime lastModifyTime { get; set; }
        public string tagId { get; set; }
    }
}

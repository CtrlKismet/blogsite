#pragma checksum "E:\Program\BlogSite\BlogSite\Views\Home\BlogDetail.cshtml" "{ff1816ec-aa5e-4d10-87f7-6f4963833460}" "620af869c16eaf812e927cab29e932e7b1d993cb"
// <auto-generated/>
#pragma warning disable 1591
[assembly: global::Microsoft.AspNetCore.Razor.Hosting.RazorCompiledItemAttribute(typeof(AspNetCore.Views_Home_BlogDetail), @"mvc.1.0.view", @"/Views/Home/BlogDetail.cshtml")]
[assembly:global::Microsoft.AspNetCore.Mvc.Razor.Compilation.RazorViewAttribute(@"/Views/Home/BlogDetail.cshtml", typeof(AspNetCore.Views_Home_BlogDetail))]
namespace AspNetCore
{
    #line hidden
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Threading.Tasks;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.AspNetCore.Mvc.Rendering;
    using Microsoft.AspNetCore.Mvc.ViewFeatures;
#line 1 "E:\Program\BlogSite\BlogSite\Views\_ViewImports.cshtml"
using BlogSite;

#line default
#line hidden
#line 1 "E:\Program\BlogSite\BlogSite\Views\Home\BlogDetail.cshtml"
using BlogSite.Models;

#line default
#line hidden
#line 2 "E:\Program\BlogSite\BlogSite\Views\Home\BlogDetail.cshtml"
using BlogSite.Controllers;

#line default
#line hidden
#line 3 "E:\Program\BlogSite\BlogSite\Views\Home\BlogDetail.cshtml"
using System.Globalization;

#line default
#line hidden
    [global::Microsoft.AspNetCore.Razor.Hosting.RazorSourceChecksumAttribute(@"SHA1", @"620af869c16eaf812e927cab29e932e7b1d993cb", @"/Views/Home/BlogDetail.cshtml")]
    [global::Microsoft.AspNetCore.Razor.Hosting.RazorSourceChecksumAttribute(@"SHA1", @"295ab12cce6caff78ba4ff7388419b3241a20df4", @"/Views/_ViewImports.cshtml")]
    public class Views_Home_BlogDetail : global::Microsoft.AspNetCore.Mvc.Razor.RazorPage<int>
    {
        private static readonly global::Microsoft.AspNetCore.Razor.TagHelpers.TagHelperAttribute __tagHelperAttribute_0 = new global::Microsoft.AspNetCore.Razor.TagHelpers.TagHelperAttribute("src", new global::Microsoft.AspNetCore.Html.HtmlString("~/js/blogdetail_script.js"), global::Microsoft.AspNetCore.Razor.TagHelpers.HtmlAttributeValueStyle.DoubleQuotes);
        #line hidden
        #pragma warning disable 0169
        private string __tagHelperStringValueBuffer;
        #pragma warning restore 0169
        private global::Microsoft.AspNetCore.Razor.Runtime.TagHelpers.TagHelperExecutionContext __tagHelperExecutionContext;
        private global::Microsoft.AspNetCore.Razor.Runtime.TagHelpers.TagHelperRunner __tagHelperRunner = new global::Microsoft.AspNetCore.Razor.Runtime.TagHelpers.TagHelperRunner();
        private global::Microsoft.AspNetCore.Razor.Runtime.TagHelpers.TagHelperScopeManager __backed__tagHelperScopeManager = null;
        private global::Microsoft.AspNetCore.Razor.Runtime.TagHelpers.TagHelperScopeManager __tagHelperScopeManager
        {
            get
            {
                if (__backed__tagHelperScopeManager == null)
                {
                    __backed__tagHelperScopeManager = new global::Microsoft.AspNetCore.Razor.Runtime.TagHelpers.TagHelperScopeManager(StartTagHelperWritingScope, EndTagHelperWritingScope);
                }
                return __backed__tagHelperScopeManager;
            }
        }
        private global::Microsoft.AspNetCore.Mvc.Razor.TagHelpers.UrlResolutionTagHelper __Microsoft_AspNetCore_Mvc_Razor_TagHelpers_UrlResolutionTagHelper;
        #pragma warning disable 1998
        public async override global::System.Threading.Tasks.Task ExecuteAsync()
        {
            BeginContext(82, 2, true);
            WriteLiteral("\r\n");
            EndContext();
#line 6 "E:\Program\BlogSite\BlogSite\Views\Home\BlogDetail.cshtml"
  
    Layout = "~/Views/Shared/_Layout.cshtml";

#line default
#line hidden
            BeginContext(150, 2, true);
            WriteLiteral("\r\n");
            EndContext();
            DefineSection("_extraCSS", async() => {
                BeginContext(172, 231, true);
                WriteLiteral("\r\n    <link href=\"https://cdnjs.loli.net/ajax/libs/github-markdown-css/3.0.1/github-markdown.min.css\" rel=\"stylesheet\">\r\n    <link href=\"https://cdnjs.loli.net/ajax/libs/highlight.js/9.15.6/styles/xcode.min.css\" rel=\"stylesheet\">\r\n");
                EndContext();
            }
            );
            BeginContext(406, 2, true);
            WriteLiteral("\r\n");
            EndContext();
            DefineSection("_extraJS", async() => {
                BeginContext(426, 201, true);
                WriteLiteral("\r\n    <script src=\"https://cdnjs.loli.net/ajax/libs/simplemde/1.11.2/simplemde.min.js\"></script>\r\n    <script src=\"https://cdnjs.loli.net/ajax/libs/highlight.js/9.15.6/highlight.min.js\"></script>\r\n    ");
                EndContext();
                BeginContext(627, 49, false);
                __tagHelperExecutionContext = __tagHelperScopeManager.Begin("script", global::Microsoft.AspNetCore.Razor.TagHelpers.TagMode.StartTagAndEndTag, "e47a7362011c46098d1bc0a2878f5a76", async() => {
                }
                );
                __Microsoft_AspNetCore_Mvc_Razor_TagHelpers_UrlResolutionTagHelper = CreateTagHelper<global::Microsoft.AspNetCore.Mvc.Razor.TagHelpers.UrlResolutionTagHelper>();
                __tagHelperExecutionContext.Add(__Microsoft_AspNetCore_Mvc_Razor_TagHelpers_UrlResolutionTagHelper);
                __tagHelperExecutionContext.AddHtmlAttribute(__tagHelperAttribute_0);
                await __tagHelperRunner.RunAsync(__tagHelperExecutionContext);
                if (!__tagHelperExecutionContext.Output.IsContentModified)
                {
                    await __tagHelperExecutionContext.SetOutputContentAsync();
                }
                Write(__tagHelperExecutionContext.Output);
                __tagHelperExecutionContext = __tagHelperScopeManager.End();
                EndContext();
                BeginContext(676, 116, true);
                WriteLiteral("\r\n    <script data-isso=\"https://isso.ctrlkismet.top/\" src=\"https://isso.ctrlkismet.top/js/embed.min.js\"></script>\r\n");
                EndContext();
            }
            );
            BeginContext(795, 2, true);
            WriteLiteral("\r\n");
            EndContext();
            DefineSection("_extraAside", async() => {
                BeginContext(819, 229, true);
                WriteLiteral("\r\n    <div class=\"menu-list\" id=\"list_of_menu\">\r\n        <div class=\"list-title\">目录</div>\r\n        <div class=\"list-item\" v-for=\"item in menu\">\r\n            <a :href=\"\'#\'+item.pos\">{{item.title}}</a>\r\n        </div>\r\n    </div>\r\n");
                EndContext();
            }
            );
            BeginContext(1051, 65, true);
            WriteLiteral("<input id=\"blog_detail_ID\" style=\"height:0;width:0;display:none;\"");
            EndContext();
            BeginWriteAttribute("value", " value=\"", 1116, "\"", 1130, 1);
#line 30 "E:\Program\BlogSite\BlogSite\Views\Home\BlogDetail.cshtml"
WriteAttributeValue("", 1124, Model, 1124, 6, false);

#line default
#line hidden
            EndWriteAttribute();
            BeginContext(1131, 42, true);
            WriteLiteral(" />\r\n<div class=\"blog\" id=\"blog_detail\">\r\n");
            EndContext();
#line 32 "E:\Program\BlogSite\BlogSite\Views\Home\BlogDetail.cshtml"
     if (Context.User.Identity.IsAuthenticated)
    {

#line default
#line hidden
            BeginContext(1229, 190, true);
            WriteLiteral("        <i class=\"fa fa-edit\" style=\"float:right;cursor:pointer;\" onclick=\"window.location.href=rootsrc+\'authorization/management?id=\'+document.getElementById(\'blog_detail_ID\').value\"></i>\r\n");
            EndContext();
#line 35 "E:\Program\BlogSite\BlogSite\Views\Home\BlogDetail.cshtml"
    }

#line default
#line hidden
            BeginContext(1426, 696, true);
            WriteLiteral(@"    <div class=""blog-header"">
        <div class=""blog-title"">{{blog.title}}</div>
        <div class=""tag-list"">
            <p style=""font-size:17px;"">标签：</p>
            <div class=""tag"" v-for=""tagName in tagsName"">{{tagName}}</div>
        </div>
    </div>
    <div style=""display: none;"">
        <textarea cols=""0"" rows=""0"" id=""blogContent"">{{blog.content}}</textarea>
    </div>
    <div class=""markdown-body blog-content""></div>
    <div class=""blog-footer"">
        <div id=""modifyedTime"">{{""最后编辑于"" + new Date(blog.lastModifyTime).toLocaleString()}}</div>
    </div>
</div>
<div class=""turn-page"" id=""pageTurning"">
    <span v-if=""pre==''""></span>
    <div class=""pre"" ");
            EndContext();
            BeginContext(2123, 186, true);
            WriteLiteral("@click=\"linkTo(-1)\" v-if=\"pre!=\'\'\">\r\n        <i class=\" fa fa-arrow-left\"></i>\r\n        <span>上一篇</span>\r\n        <span class=\"ellipsis\">{{pre}}</span>\r\n    </div>\r\n    <div class=\"nxt\" ");
            EndContext();
            BeginContext(2310, 208, true);
            WriteLiteral("@click=\"linkTo(1)\" v-if=\"nxt!=\'\'\">\r\n        <span>下一篇</span>\r\n        <span class=\"ellipsis\">{{nxt}}</span>\r\n        <i class=\"fa fa-arrow-right\"></i>\r\n    </div>\r\n</div>\r\n<section id=\"isso-thread\"></section>");
            EndContext();
        }
        #pragma warning restore 1998
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.ViewFeatures.IModelExpressionProvider ModelExpressionProvider { get; private set; }
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.IUrlHelper Url { get; private set; }
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.IViewComponentHelper Component { get; private set; }
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.Rendering.IJsonHelper Json { get; private set; }
        [global::Microsoft.AspNetCore.Mvc.Razor.Internal.RazorInjectAttribute]
        public global::Microsoft.AspNetCore.Mvc.Rendering.IHtmlHelper<int> Html { get; private set; }
    }
}
#pragma warning restore 1591

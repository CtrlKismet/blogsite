#pragma checksum "E:\Program\BlogSite\BlogSite\Views\Home\About.cshtml" "{ff1816ec-aa5e-4d10-87f7-6f4963833460}" "6b94d1194d695504ae25ec9bdf4cbbbd64dbb385"
// <auto-generated/>
#pragma warning disable 1591
[assembly: global::Microsoft.AspNetCore.Razor.Hosting.RazorCompiledItemAttribute(typeof(AspNetCore.Views_Home_About), @"mvc.1.0.view", @"/Views/Home/About.cshtml")]
[assembly:global::Microsoft.AspNetCore.Mvc.Razor.Compilation.RazorViewAttribute(@"/Views/Home/About.cshtml", typeof(AspNetCore.Views_Home_About))]
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
#line 1 "E:\Program\BlogSite\BlogSite\Views\Home\About.cshtml"
using BlogSite.Models;

#line default
#line hidden
#line 2 "E:\Program\BlogSite\BlogSite\Views\Home\About.cshtml"
using BlogSite.Controllers;

#line default
#line hidden
#line 3 "E:\Program\BlogSite\BlogSite\Views\Home\About.cshtml"
using System.Globalization;

#line default
#line hidden
    [global::Microsoft.AspNetCore.Razor.Hosting.RazorSourceChecksumAttribute(@"SHA1", @"6b94d1194d695504ae25ec9bdf4cbbbd64dbb385", @"/Views/Home/About.cshtml")]
    [global::Microsoft.AspNetCore.Razor.Hosting.RazorSourceChecksumAttribute(@"SHA1", @"295ab12cce6caff78ba4ff7388419b3241a20df4", @"/Views/_ViewImports.cshtml")]
    public class Views_Home_About : global::Microsoft.AspNetCore.Mvc.Razor.RazorPage<int>
    {
        private static readonly global::Microsoft.AspNetCore.Razor.TagHelpers.TagHelperAttribute __tagHelperAttribute_0 = new global::Microsoft.AspNetCore.Razor.TagHelpers.TagHelperAttribute("src", new global::Microsoft.AspNetCore.Html.HtmlString("~/js/blogdetail_script.js"), global::Microsoft.AspNetCore.Razor.TagHelpers.HtmlAttributeValueStyle.DoubleQuotes);
        private static readonly global::Microsoft.AspNetCore.Razor.TagHelpers.TagHelperAttribute __tagHelperAttribute_1 = new global::Microsoft.AspNetCore.Razor.TagHelpers.TagHelperAttribute("src", new global::Microsoft.AspNetCore.Html.HtmlString("~/images/head.jpg"), global::Microsoft.AspNetCore.Razor.TagHelpers.HtmlAttributeValueStyle.DoubleQuotes);
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
#line 6 "E:\Program\BlogSite\BlogSite\Views\Home\About.cshtml"
  
    ViewData["Title"] = "关于CtrlKismet";
    Layout = "~/Views/Shared/_Layout.cshtml";

#line default
#line hidden
            BeginContext(191, 2, true);
            WriteLiteral("\r\n");
            EndContext();
            DefineSection("_extraCSS", async() => {
                BeginContext(213, 231, true);
                WriteLiteral("\r\n    <link href=\"https://cdnjs.loli.net/ajax/libs/github-markdown-css/3.0.1/github-markdown.min.css\" rel=\"stylesheet\">\r\n    <link href=\"https://cdnjs.loli.net/ajax/libs/highlight.js/9.15.6/styles/xcode.min.css\" rel=\"stylesheet\">\r\n");
                EndContext();
            }
            );
            BeginContext(447, 2, true);
            WriteLiteral("\r\n");
            EndContext();
            DefineSection("_extraJS", async() => {
                BeginContext(467, 201, true);
                WriteLiteral("\r\n    <script src=\"https://cdnjs.loli.net/ajax/libs/simplemde/1.11.2/simplemde.min.js\"></script>\r\n    <script src=\"https://cdnjs.loli.net/ajax/libs/highlight.js/9.15.6/highlight.min.js\"></script>\r\n    ");
                EndContext();
                BeginContext(668, 49, false);
                __tagHelperExecutionContext = __tagHelperScopeManager.Begin("script", global::Microsoft.AspNetCore.Razor.TagHelpers.TagMode.StartTagAndEndTag, "338d27dd67fd46c2a5cc3faeb2bb47ae", async() => {
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
                BeginContext(717, 173, true);
                WriteLiteral("\r\n    <script>\r\n        scrollValue = 600;\r\n    </script>\r\n    <script data-isso=\"https://isso.ctrlkismet.top/\" src=\"https://isso.ctrlkismet.top/js/embed.min.js\"></script>\r\n");
                EndContext();
            }
            );
            BeginContext(893, 2, true);
            WriteLiteral("\r\n");
            EndContext();
            DefineSection("_extraSculptrue", async() => {
                BeginContext(920, 29, true);
                WriteLiteral("\r\n    <div class=\"sculptrue\">");
                EndContext();
                BeginContext(949, 29, false);
                __tagHelperExecutionContext = __tagHelperScopeManager.Begin("img", global::Microsoft.AspNetCore.Razor.TagHelpers.TagMode.StartTagOnly, "ad990893de284d4683ddffb2c0869930", async() => {
                }
                );
                __Microsoft_AspNetCore_Mvc_Razor_TagHelpers_UrlResolutionTagHelper = CreateTagHelper<global::Microsoft.AspNetCore.Mvc.Razor.TagHelpers.UrlResolutionTagHelper>();
                __tagHelperExecutionContext.Add(__Microsoft_AspNetCore_Mvc_Razor_TagHelpers_UrlResolutionTagHelper);
                __tagHelperExecutionContext.AddHtmlAttribute(__tagHelperAttribute_1);
                await __tagHelperRunner.RunAsync(__tagHelperExecutionContext);
                if (!__tagHelperExecutionContext.Output.IsContentModified)
                {
                    await __tagHelperExecutionContext.SetOutputContentAsync();
                }
                Write(__tagHelperExecutionContext.Output);
                __tagHelperExecutionContext = __tagHelperScopeManager.End();
                EndContext();
                BeginContext(978, 8, true);
                WriteLiteral("</div>\r\n");
                EndContext();
            }
            );
            BeginContext(989, 2, true);
            WriteLiteral("\r\n");
            EndContext();
            DefineSection("_extraAside", async() => {
                BeginContext(1013, 229, true);
                WriteLiteral("\r\n    <div class=\"menu-list\" id=\"list_of_menu\">\r\n        <div class=\"list-title\">目录</div>\r\n        <div class=\"list-item\" v-for=\"item in menu\">\r\n            <a :href=\"\'#\'+item.pos\">{{item.title}}</a>\r\n        </div>\r\n    </div>\r\n");
                EndContext();
            }
            );
            BeginContext(1245, 67, true);
            WriteLiteral("\r\n<input id=\"blog_detail_ID\" style=\"height:0;width:0;display:none;\"");
            EndContext();
            BeginWriteAttribute("value", " value=\"", 1312, "\"", 1326, 1);
#line 39 "E:\Program\BlogSite\BlogSite\Views\Home\About.cshtml"
WriteAttributeValue("", 1320, Model, 1320, 6, false);

#line default
#line hidden
            EndWriteAttribute();
            BeginContext(1327, 511, true);
            WriteLiteral(@" />
<div class=""blog about"" id=""blog_detail"">
    <div class=""blog-header"">
        <div class=""blog-title"">{{blog.title}}</div>
    </div>
    <div style=""display: none;"">
        <textarea cols=""0"" rows=""0"" id=""blogContent"">{{blog.content}}</textarea>
    </div>
    <div class=""markdown-body blog-content""></div>
    <div class=""blog-footer"">
        <div id=""modifyedTime"">{{""最后编辑于"" + new Date(blog.lastModifyTime).toLocaleString()}}</div>
    </div>
</div>
<section id=""isso-thread""></section>");
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

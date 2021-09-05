let smde = new SimpleMDE({
    element: document.getElementById("blogContent"),
    autoDownloadFontAwesome: false,
    spellChecker: false,
    status: false,
    tabSize: 4
});

let blogDetail = new Vue({
    el: "#blog_detail",
    data: {
        blog: {
            id: -1,
            title: "",
            content: "",
            lastModifyTime: ""
        },
        tagsName: []
    },
    mounted: function () {
        let filter = {
            id: $('#blog_detail_ID')[0].value,
            needReturn: "110101"
        };

        $.ajax({
            url: rootsrc + 'api/blog',
            type: "get",
            contentType: "application/json",
            dataType: "json",
            data: {
                jsonFilter: JSON.stringify(filter)
            },
            success: function (blogData) {
                blogDetail.blog = blogData[0];
                document.title = blogData[0].title + " | CtrlKismet's Blog";
                if (filter.id == 0) {
                    RenderMarkdown(blogData[0].content);
                    return;
                }
                $.ajax({
                    type: "get",
                    url: rootsrc + "api/tag/" + blogData[0].id,
                    success: function (tags) {
                        blogDetail.tagsName = tags;
                        RenderMarkdown(blogData[0].content);
                    }
                });
            }
        });
    }
});

let menu_index = 0;

let menus = new Vue({
    el: "#list_of_menu",
    data: {
        menu: []
    },
    methods: {
        get_menu: function () {
            $('.blog-content')[0].childNodes.forEach(function (value) {
                if (value.id) {
                    Vue.set(menus.menu, menu_index, {
                        title: value.innerText,
                        pos: menu_index + 1
                    });
                    menu_index++;
                    value.id = menu_index;
                }
            });
            this.$nextTick(function () {
                $('.menu-list')[0].children[1].classList.add("list-item-active");
            });
        }
    },
});

function RenderMarkdown(content) {
    $(".blog-content")[0].innerHTML = smde.markdown(content);
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });
    smde.toTextArea();
    MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    menus.get_menu();
    loadEl();
}

let preOrnxt = new Vue({
    el: '#pageTurning',
    data: {
        pre: "",
        nxt: ""
    },
    mounted: function () {
        $.ajax({
            type: "get",
            url: rootsrc + "api/blog/" + $('#blog_detail_ID')[0].value,
            success: function (blogsName) {
                preOrnxt.pre = blogsName[0];
                preOrnxt.nxt = blogsName[1];
            }
        });
    },
    methods: {
        linkTo: function (value) {
            var nid = parseInt($('#blog_detail_ID')[0].value) + value;
            window.location.href = rootsrc + 'home/blogdetail/' + nid;
        }
    }
});

let pre_index = 1;

document.addEventListener('scroll', function () {
    for (let now_index = 0; now_index < menu_index; now_index++) {
        const el = document.getElementById(now_index + 1);
        if (window.scrollY < el.offsetTop) {
            if (pre_index === now_index || now_index == 0) break;
            $('.menu-list')[0].children[pre_index].classList.remove("list-item-active");
            $('.menu-list')[0].children[now_index].classList.add("list-item-active");
            pre_index = now_index;
            break;
        } else if (now_index === menu_index - 1) {
            $('.menu-list')[0].children[pre_index].classList.remove("list-item-active");
            $('.menu-list')[0].children[menu_index].classList.add("list-item-active");
            pre_index = menu_index;
        }
    }

    for (let now_index = 0; now_index < menu_index; now_index++) {
        if (pre_index !== now_index) {
            $('.menu-list')[0].children[now_index].classList.remove("list-item-active");
        }
    }
});
let homePage = new Vue({
    el: "#home",
    data: {
        blog: [],
        message: "",
        isFilter: false
    },
    mounted: function () {
        this.getAllBlog();
        loadEl();
    },
    methods: {
        transMsg: function (data) {
            homePage.blog = data;
            $.each(data, function (idx, value) {
                homePage.blog[idx].id = value.id;
                homePage.blog[idx].url = rootsrc + "home/blogdetail/" + value.id;
                let addTime = new Date(homePage.blog[idx].addTime);
                homePage.blog[idx].addYear = addTime.getFullYear();
                homePage.blog[idx].addMonthDay = (addTime.getMonth() + 1) + '/' + addTime.getDate();
            });
        },
        getAllBlog: function () {
            let filter = {
                id: -1,
                needReturn: "111010"
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
                    homePage.transMsg(blogData);
                }
            });
        },
        linkTo: function (url) {
            Window.location.href = url;
        },
        removeFilter: function () {
            homePage.isFilter = false;
            homePage.message = "";
            homePage.getAllBlog();
        }
    }
});

Vue.component('blog-article', {
    props: {
        title: "",
        ellipsisContent: "",
        addYear: "",
        addMonthDay: "",
        url: ""
    },
    template: '<div class="article">  \
                    <div class="time-stamp"> \
                        <p>{{addYear}}</p> \
                        <hr /> \
                        <p>{{addMonthDay}}</p> \
                    </div> \
                    <div class="art-content" @click="linkTo(url)"> \
                        <a :href="url"><div class="art-title ellipsis">{{title}}</div></a> \
                        <a :href="url"><div class="art-ellipsis">{{ellipsisContent}}</div></a> \
                    </div> \
                </div>'
});

let tagList = new Vue({
    el: "#list_of_tags",
    data: {
        tag: []
    },
    mounted: function () {
        $.get(rootsrc + "api/tag",
            function (tagData) {
                tagList.tag = tagData;
            }
        );
    },
    methods: {
        search_blog_by_tagid: function (id, name) {
            $('body,html').css('scroll-behavior', 'auto');
            $('body,html').scrollTop(0);
            $('body,html').css('scroll-behavior', 'smooth');
            let filter = {
                id: -1,
                tagId: id + ';',
                needReturn: "111010"
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
                    homePage.isFilter = true;
                    homePage.message = name;
                    homePage.transMsg(blogData);
                }
            });
        }
    }
});
let blog_arch = {
    props: {
        blog: {
            type: Object,
            default: {
                title: "",
                url: "",
                time: ""
            }
        }
    },
    template: '<div class="blog-detail"> \
                    <div class="fa fa-circle archive-points"></div> \
                    <div class="ellipsis"><a :href="blog.url">{{blog.title}}</a></div> \
                    <div>{{blog.time}}</div> \
                </div>'
};

let augment = {
    props: {
        data: {
            type: Object,
            default: {
                title: "",
                url: "",
                time: ""
            }
        }
    },
    template: "<div>{{data.title}}</div>"
}

let archive_blog = {
    props: {
        blog_msg: {
            type: Array
        },
        i: {
            type: Number
        }
    },
    template: '<div class="blog-archive"> \
                    <div class="archive-header"> \
                    <div class="blog-year">{{(timeYear-i)}}</div> \
                    <div></div> \
                    <div>{{"共"+count[i]+"篇"}}</div> \
                </div> \
                <div class="archive-content"> \
                    <blog_arch v-for="(blog,index) in blog_msg" :blog="blog" :key="index"></blog_arch> \
                </div> \
                <div class="archive-footer"></div> \
                </div>',
    components: {
        blog_arch,
        augment
    },
    data() {
        return {
            timeYear: homePage.blog_timeYear,
            count: homePage.blog_count
        }
    }
};

let homePage = new Vue({
    el: "#home",
    data: {
        blog_msg: [],
        blog_timeYear: new Date().getFullYear(),
        blog_count: [0, 0, 0],
        total_count: 0
    },
    mounted: function () {
        this.getAllBlog();
        loadEl();
    },
    methods: {
        transMsg: function (data) {
            let year_now = 0,
                year_i = -1,
                blog_i = 0,
                year, blogs = [];
            $.each(data, function (idx, value) {
                let addTime = new Date(value.addTime);
                year = addTime.getFullYear();
                if (year !== year_now) {
                    year_now = year;
                    Vue.set(homePage.blog_count, year_i, blog_i);
                    year_i++;
                    homePage.total_count += blog_i;
                    blog_i = 0;
                    blogs.push([]);
                }
                blogs[year_i].push(new Object({
                    id: value.id,
                    title: value.title,
                    url: rootsrc + "home/blogdetail/" + value.id,
                    time: (addTime.getMonth() + 1) + '/' + addTime.getDate()
                }));
                blog_i++;
            });
            Vue.set(homePage.blog_count, year_i, blog_i);
            homePage.total_count += blog_i;
            homePage.blog_msg = blogs;
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
        getCount: function (id) {
            return homePage.blog_msg[id][0].addTime.getFullYear() + '年共' + homePage.blog_msg[id].length + '篇';
        }
    },
    components: {
        archive_blog
    }
});

function test() {
    homePage.blog_msg.forEach((index, value) => {
        console.log(index)
        console.log(typeof (index))
    });
}
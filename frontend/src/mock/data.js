/**
 * Mock 数据模块 — 用于前端开发预览
 * 后端 API 就绪后删除此文件，切换到真实 API 调用
 */
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
})

// ===== About 页面内容 =====
const aboutMarkdown = `# 关于我

> 关于界面的文字

### 写在前面

其实写这个博客是大一下学期时就想做的事情了，但是碍于自己实在是太懒了（其实完全不是因为搞ACM之类的事情一直比较忙）

拖着拖着来到了大二下，之间一直都是浑浑噩噩的生活着，到了大三之后突然发现这么多年来是不是没有真的好好地思考过之后的事情呢？明明有这么多的小九九（碎碎念念的），但总是没有按照自己的想法，没有做出真正属于自己的选择，为什么不试着去尝试一下呢？于是出现了一系列非常愚蠢的决定（详见之后可能随缘更新的随笔吧），直到快大三上期末的时候终于开始填博客的坑了。

### 自我介绍

地道的弗兰人一枚，曾经有一口标准的~~塑料~~普通话，现在只有在湖南才能说出来了。
* 奔三的年纪，性别男爱好女。兴趣十分的废柴(会的不**少**懂得不**多**)；
* 对艺术类的事情有一种近乎**偏执**的**三分钟热度**；
* 学习(或者接触)过的兴趣包括但不限于架子鼓、ukulele、画画、篮球、乒乓球、游泳……；
* 在某些地方非常的**过时**，但某些地方又十分关注**前沿**；
* 喜欢幻想但并不中二，自从发现B站弹幕功能起便半只脚踏入了二次元；
* 属于steam喜$+1$用户，十分沉醉于剧情向游戏；
* 总是喜欢向身边的朋友说自己比较**内向**，但对于这些听我说起过我算内向的人就会变成不折不扣的**话痨**；
* 很喜欢发空间且执着的喜欢配图；

### 个人能力

初中的时候学习过数学竞赛。高中的时候被分配到信息竞赛，开始了一段永生难忘的竞赛生活。大学的时候进入ACM的坑，最后只拿到银遗憾退役。

大一时被科协学长带入web坑，从此一发不可收拾。对于C++、C#较为熟悉，java、python有所涉猎；前端框架只会使用十分简陋的vue；对于linux有所了解。

### 写在最后

感谢您的阅读~，欢迎来找我玩。`

// ===== 文章 1 =====
const article1Markdown = `# 永远相信美好的事情即将发生

> Always believe that something wonderful is about to happen.

永远相信美好的事情即将发生。
Always believe that something wonderful is about to happen.

> 或许前路永夜，即便如此我也要前进，因为即使星光微弱也会为我照亮前路。 ——『四月是你的谎言』`

// ===== 文章 2 =====
const article2Markdown = `# 博客开发进度汇总

> 基本功能写完了，剩下的期末之后再填坑

### 做完了的事情
**基本**功能实现了~~（事实上并不能新建标签）~~

### 还要做的事
疯狂填坑，包括但不限于：

* ~~实现新建标签~~
* 友链
* ~~写完About界面~~
* ~~文章的编辑（目前只能暴力修改数据库）~~
* ~~这个奇怪的底边栏~~
* ~~增加博客详情的上一篇下一篇~~
* ~~上传时间提早了8个小时~~
* ~~页面语言设置为中文~~
* ~~LaTeX字体大小调整~~
* ~~首页单个条目的高度过渡设置~~

### 还想做的事
继填坑之后当然应该挖更大的坑了(雾)，包括但不限于：

* **响应式布局！！！**
* ~~LaTeX的支持~~
* ~~增加了Markdown中代码块的代码高亮~~
* ~~图片、~~音乐等等的插入
* 图片加载速度太慢
* 文件导入博客
* ~~设置进入页面的过渡动画（比如顶栏的淡入）~~
* ~~增加了administrator的登录~~
* ~~回到顶部按钮~~
* ~~归档~~
* ~~进行了ssl认证~~

### 最后的最后
考研要加油呀！！！

***Bless All.***`

// ===== Mock 标签 =====
const mockTags = [
  { id: 1, name: '技术' },
  { id: 2, name: '随笔' },
  { id: 3, name: '生活' }
]

// ===== Mock 文章列表 =====
const mockArticles = [
  {
    id: 1,
    title: '永远相信美好的事情即将发生',
    summary: 'Always believe that something wonderful is about to happen.',
    status: 'published',
    published_at: '2018-12-18T00:00:00',
    updated_at: '2018-12-18T00:00:00',
    tags: [mockTags[1]]
  },
  {
    id: 2,
    title: '博客开发进度汇总',
    summary: '基本功能写完了，剩下的期末之后再填坑',
    status: 'published',
    published_at: '2018-12-27T00:00:00',
    updated_at: '2019-02-23T00:00:00',
    tags: [mockTags[0]]
  }
]

// ===== Mock 文章详情 =====
const mockArticleDetails = {
  1: {
    ...mockArticles[0],
    content_html: md.render(article1Markdown),
    header_image: null
  },
  2: {
    ...mockArticles[1],
    content_html: md.render(article2Markdown),
    header_image: null
  }
}

// ===== Mock About =====
const mockAbout = {
  id: 0,
  title: '关于我',
  content_html: md.render(aboutMarkdown),
  published_at: '2018-12-18T00:00:00',
  updated_at: '2018-12-18T00:00:00'
}

// ===== Mock 归档 =====
const mockArchive = [
  {
    year: 2018,
    articles: [
      { id: 2, title: '博客开发进度汇总', published_at: '2018-12-27T00:00:00' },
      { id: 1, title: '永远相信美好的事情即将发生', published_at: '2018-12-18T00:00:00' }
    ]
  }
]

// ===== 导出模拟 API =====
export const useMock = true

export function mockGetArticles(params = {}) {
  let items = [...mockArticles]
  if (params.tag_id) {
    items = items.filter(a => a.tags.some(t => t.id === params.tag_id))
  }
  return Promise.resolve({
    data: { items, total: items.length, page: 1, size: 20 }
  })
}

export function mockGetArticle(id) {
  const detail = mockArticleDetails[id]
  if (detail) return Promise.resolve({ data: detail })
  return Promise.reject({ response: { status: 404 } })
}

export function mockGetAbout() {
  return Promise.resolve({ data: mockAbout })
}

export function mockGetArchive() {
  return Promise.resolve({ data: mockArchive })
}

export function mockGetTags() {
  return Promise.resolve({ data: mockTags })
}

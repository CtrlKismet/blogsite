/**
 * 页面可见性处理
 * 实现页面失焦时切换标题和 Favicon 的功能
 */
let originalTitle = ''

const FAVICON_IN = '/faviconIN.ico'
const FAVICON_OUT = '/faviconOUT.ico'
const HIDDEN_TITLE = '这里是CtrlKismet的博客'

function setFavicon(href: string): void {
  let link = document.querySelector("link[rel~='icon']") as HTMLLinkElement | null
  if (!link) {
    link = document.createElement('link')
    link.rel = 'icon'
    document.head.appendChild(link)
  }
  link.href = href
}

function handleVisibilityChange(): void {
  if (document.hidden) {
    originalTitle = document.title
    document.title = HIDDEN_TITLE
    setFavicon(FAVICON_OUT)
  } else {
    document.title = originalTitle
    setFavicon(FAVICON_IN)
  }
}

/**
 * 初始化页面可见性监听
 */
export function initVisibility(): void {
  setFavicon(FAVICON_IN)
  document.addEventListener('visibilitychange', handleVisibilityChange)
}

/**
 * 销毁页面可见性监听
 */
export function destroyVisibility(): void {
  document.removeEventListener('visibilitychange', handleVisibilityChange)
}



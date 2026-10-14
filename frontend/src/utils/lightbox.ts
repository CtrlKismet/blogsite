import type Viewer from 'viewerjs'
import 'viewerjs/dist/viewer.css'
import '../styles/lightbox.css'

const LABELS: Record<string, string> = {
  mix: '关闭', zoomIn: '放大', zoomOut: '缩小', oneToOne: '原始尺寸',
  reset: '适应窗口', prev: '上一张', next: '下一张',
}

/** Bind the gallery now; load the viewer and original images only on demand. */
export function attachImageLightbox(container: HTMLElement): () => void {
  let viewer: Viewer | null = null
  let pending: Promise<void> | null = null
  let disposed = false
  let selectedIndex = 0
  let trigger: HTMLAnchorElement | null = null
  const images = [...container.querySelectorAll<HTMLImageElement>('img[data-lightbox-src]')]

  async function open(event: MouseEvent): Promise<void> {
    if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return
    const link = (event.target as Element).closest<HTMLAnchorElement>('a.image-lightbox-link')
    if (!link || !container.contains(link)) return
    const image = link.querySelector<HTMLImageElement>('img[data-lightbox-src]')
    if (!image) return
    event.preventDefault()
    event.stopPropagation()
    selectedIndex = images.indexOf(image)
    if (selectedIndex < 0) return
    trigger = link
    try {
      if (!pending) {
        pending = import('viewerjs').then(({ default: ImageViewer }) => {
          if (disposed) return
          viewer = new ImageViewer(container, {
            className: 'blog-lightbox',
            zIndex: 11000,
            transition: { view: false },
            filter: (img) => images.includes(img),
            url: (img) => img.dataset.lightboxSrc || img.src,
            inheritedAttributes: ['crossOrigin', 'referrerPolicy', 'decoding'],
            navbar: false,
            title: (img) => img.alt || '',
            toolbar: {
              zoomIn: true, zoomOut: true, oneToOne: true, reset: true,
              prev: images.length > 1, next: images.length > 1,
            },
            navigation: images.length > 1,
            loop: false,
            preload: false,
            keyboard: true,
            focus: true,
            fullscreen: false,
            maxZoomRatio: 8,
            ready() {
              const root = document.querySelector<HTMLElement>('.blog-lightbox')
              if (!root) return
              root.setAttribute('aria-label', '图片查看器')
              root.querySelectorAll<HTMLElement>('[data-viewer-action]').forEach((control) => {
                const label = LABELS[control.dataset.viewerAction || '']
                if (!label) return
                control.title = label
                control.setAttribute('aria-label', label)
                control.removeAttribute('aria-hidden')
                control.tabIndex = 0
              })
            },
            hidden() {
              if (!disposed && trigger?.isConnected) trigger.focus({ preventScroll: true })
            },
          })
        })
      }
      await pending
      if (!disposed) viewer?.view(selectedIndex)
    } catch (error) {
      pending = null
      console.error('图片查看器加载失败', error)
      if (!disposed) window.location.assign(link.href)
    }
  }

  container.addEventListener('click', open, true)
  return () => {
    disposed = true
    container.removeEventListener('click', open, true)
    viewer?.destroy()
    viewer = null
  }
}

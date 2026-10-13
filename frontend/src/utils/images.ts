export function prepareImageHtml(html: string): string {
  // Transform before insertion so the browser never starts downloading originals.
  const template = document.createElement('template')
  template.innerHTML = html
  template.content.querySelectorAll<HTMLImageElement>('img').forEach((img, index) => {
    img.decoding = 'async'
    img.loading = index === 0 ? 'eager' : 'lazy'
    let original: URL
    try {
      original = new URL(img.getAttribute('src') || '', window.location.href)
    } catch {
      return
    }
    if (original.origin !== window.location.origin || !original.pathname.startsWith('/api/v1/images/')) return
    const preview = (width: number) => {
      const url = new URL(original)
      url.searchParams.set('w', String(width))
      return url.pathname + url.search
    }
    img.srcset = [640, 1280, 1920].map((width) => `${preview(width)} ${width}w`).join(', ')
    img.sizes = '(max-width: 768px) 100vw, 960px'
    img.src = preview(1280)
    if (!img.closest('a')) {
      const link = document.createElement('a')
      link.href = original.href
      link.target = '_blank'
      link.rel = 'noopener'
      link.title = '查看原图'
      img.replaceWith(link)
      link.appendChild(img)
    }
  })
  return template.innerHTML
}

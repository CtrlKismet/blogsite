async function copyCode(text: string): Promise<void> {
  if (navigator.clipboard?.writeText) {
    try {
      await navigator.clipboard.writeText(text)
      return
    } catch { /* Fall back when clipboard permission is unavailable. */ }
  }
  const focused = document.activeElement as HTMLElement | null
  const textarea = document.createElement('textarea')
  textarea.value = text
  textarea.style.position = 'fixed'
  textarea.style.opacity = '0'
  textarea.setAttribute('readonly', '')
  document.body.appendChild(textarea)
  try {
    textarea.select()
    if (!document.execCommand('copy')) throw new Error('Clipboard unavailable')
  } finally {
    textarea.remove()
    focused?.focus({ preventScroll: true })
  }
}

export function prepareCodeBlocks(container: HTMLElement): void {
  container.querySelectorAll<HTMLElement>('pre > code').forEach((code) => {
    const pre = code.parentElement!
    if (pre.parentElement?.classList.contains('code-block')) return
    const wrapper = document.createElement('div')
    wrapper.className = 'code-block'
    const toolbar = document.createElement('div')
    toolbar.className = 'code-toolbar'
    const language = document.createElement('span')
    language.className = 'code-language'
    const languageClass = [...code.classList].find((name) => name.startsWith('language-'))
    language.textContent = languageClass?.slice('language-'.length) || 'text'
    const button = document.createElement('button')
    button.type = 'button'
    button.className = 'code-copy'
    button.textContent = '复制'
    button.setAttribute('aria-label', '复制代码')
    button.setAttribute('aria-live', 'polite')
    button.addEventListener('click', async () => {
      if (button.disabled) return
      button.disabled = true
      try {
        await copyCode(code.textContent || '')
        button.textContent = '已复制'
      } catch {
        button.textContent = '复制失败'
      } finally {
        setTimeout(() => {
          button.textContent = '复制'
          button.disabled = false
        }, 1600)
      }
    })
    toolbar.append(language, button)
    pre.replaceWith(wrapper)
    wrapper.append(toolbar, pre)
    pre.tabIndex = 0
    pre.setAttribute('aria-label', `${language.textContent} 代码，可滚动查看`)
  })
}

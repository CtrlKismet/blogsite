import katex from 'katex'

/**
 * Render LaTeX math expressions inside a DOM element using KaTeX.
 *
 * The backend's dollarmath_plugin already converts:
 *   $...$   → <span class="math inline">...</span>
 *   $$...$$ → <div class="math block">...</div>
 *
 * This function finds those elements and renders the LaTeX with KaTeX.
 * Call after v-html content is mounted (i.e. in nextTick).
 */
export function renderMath(el: HTMLElement): void {
  // Inline math: <span class="math inline">...</span>
  el.querySelectorAll('span.math.inline').forEach((span) => {
    const tex = span.textContent || ''
    try {
      katex.render(tex, span as HTMLElement, { displayMode: false, throwOnError: false })
    } catch { /* ignore */ }
  })

  // Display math: <div class="math block">...</div>
  el.querySelectorAll('div.math.block').forEach((div) => {
    const tex = div.textContent || ''
    try {
      katex.render(tex, div as HTMLElement, { displayMode: true, throwOnError: false })
    } catch { /* ignore */ }
  })
}

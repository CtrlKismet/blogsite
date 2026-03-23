import renderMathInElement from 'katex/dist/contrib/auto-render.mjs'

/**
 * Render LaTeX math expressions inside a DOM element using KaTeX.
 * Call after v-html content is mounted (i.e. in nextTick).
 */
export function renderMath(el: HTMLElement): void {
  renderMathInElement(el, {
    delimiters: [
      { left: '$$', right: '$$', display: true },
      { left: '$', right: '$', display: false },
    ],
    throwOnError: false,
  })
}

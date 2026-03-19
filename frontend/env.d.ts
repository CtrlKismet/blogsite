/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

declare module '@vscode/markdown-it-katex' {
  import type MarkdownIt from 'markdown-it'
  const plugin: { default: MarkdownIt.PluginSimple }
  export default plugin
}

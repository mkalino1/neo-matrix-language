import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Neo Language",
  description: "Docs and online editor for Neo programming language",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Editor', link: '/editor' }
    ],

    sidebar: [
      {
        text: 'Main menu',
        items: [
          { text: 'Get Started', link: '/get-started' },
          { text: 'Editor', link: '/editor' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/mkalino1/neo-matrix-language' }
    ]
  }
})

import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Neo Matrix Language",
  description: "A friendly functional programming language with matrix operations",
  head: [
    ['link', { rel: 'icon', href: '/logo.png' }],
  ],

  themeConfig: {
    logo: '/logo.png',

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

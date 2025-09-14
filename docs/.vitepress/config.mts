import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "Neo Matrix Language",
  description: "A friendly functional programming language with matrix operations",
  head: [
    ['link', { rel: 'icon', href: './logo.png' }],
  ],

  themeConfig: {
    logo: './logo.png',

    nav: [
      { text: 'Home', link: '/' },
      { text: 'Get Started', link: '/get-started' },
      { text: 'Editor', link: '/editor' }
    ],

    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'Introduction', link: '/get-started/' },
          { text: 'Editor', link: '/editor' },
          { text: 'Quick Start', link: '/get-started/quick-start' }
        ]
      }
    ],

    socialLinks: [
      { icon: 'github', link: 'https://github.com/mkalino1/neo-matrix-language' }
    ],

    search: {
      provider: 'local'
    },

    footer: {
      message: 'Made with ❤️ by Mateusz Kalinowski'
    },

    lastUpdated: {
      text: 'Last updated',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'medium'
      }
    }
  }
})

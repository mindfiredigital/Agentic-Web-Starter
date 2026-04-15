import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const githubRepo = 'https://github.com/thiga-mindfire/agentic_web_starter';

const config: Config = {
  title: 'Agentic Web Starter',
  tagline: 'FastAPI agentic RAG backend — project documentation',
  favicon: 'img/favicon.ico',

  future: {
    v4: true,
  },

  // For GitHub Pages (project site), set url/baseUrl e.g. https://<user>.github.io and /agentic_web_starter/
  url: 'https://thiga-mindfire.github.io',
  baseUrl: '/',

  organizationName: 'thiga-mindfire',
  projectName: 'agentic_web_starter',

  onBrokenLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          path: '../docs',
          sidebarPath: './sidebars.ts',
          editUrl: `${githubRepo}/edit/main/docs/`,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Agentic Web Starter',
      logo: {
        alt: 'Agentic Web Starter',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: githubRepo,
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Repository README',
              href: `${githubRepo}/blob/main/README.md`,
            },
          ],
        },
        {
          title: 'Repository',
          items: [
            {
              label: 'GitHub',
              href: githubRepo,
            },
            {
              label: 'Issues',
              href: `${githubRepo}/issues`,
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Agentic Web Starter contributors. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

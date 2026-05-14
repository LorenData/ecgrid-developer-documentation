// AI Attribution — Loren Data AI Use Policy §8.2
// Tool:        Claude Code (Anthropic)
// 2026-05-07: Initial ECGrid Developer Documentation Portal config - Greg Kolinski
// 2026-05-08: Add Guides navbar item and footer link - Greg Kolinski
// 2026-05-08: Switch to GitHub Pages default domain (lorendata.github.io) - Greg Kolinski
// 2026-05-08: Fix footer Getting Started link; remove intro.md reference - Greg Kolinski
// 2026-05-12: Add Transformation API navbar link and footer Live Reference - Greg Kolinski
// 2026-05-12: Add Catalog API navbar link and footer Live Reference - Greg Kolinski
// 2026-05-13: Fix typo in repo name — documention → documentation (baseUrl, editUrl, GitHub links) - Greg Kolinski
// 2026-05-13: Revert url/baseUrl to GitHub Pages with corrected repo name spelling - Greg Kolinski
// 2026-05-14: Switch to custom domain api.ecgridos.io; add CNAME; set baseUrl to / - Greg Kolinski

import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

const config: Config = {
  title: "ECGrid Developer Documentation Portal",
  tagline: "REST and SOAP API documentation for the ECGrid B2B platform",
  favicon: "img/favicon.ico",

  future: {
    v4: true,
  },

  url: "https://api.ecgridos.io",
  baseUrl: "/",

  organizationName: "LorenData",
  projectName: "ecgrid-developer-portal",
  deploymentBranch: "gh-pages",
  trailingSlash: false,

  onBrokenLinks: "warn",
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: "warn",
    },
  },

  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  // docusaurus-plugin-openapi-docs requires a clean npm install before enabling.
  // Re-enable after running: npm install docusaurus-plugin-openapi-docs docusaurus-theme-openapi-docs
  // plugins: [
  //   [
  //     "docusaurus-plugin-openapi-docs",
  //     {
  //       id: "ecgrid-rest-api",
  //       docsPluginId: "classic",
  //       config: {
  //         ecgrid: {
  //           specPath: "https://rest.ecgrid.io/swagger/v2/swagger.json",
  //           outputDir: "docs/rest-api/generated",
  //           sidebarOptions: {
  //             groupPathsBy: "tag",
  //             categoryLinkSource: "tag",
  //           },
  //         },
  //       },
  //     },
  //   ],
  // ],

  presets: [
    [
      "classic",
      {
        docs: {
          sidebarPath: "./sidebars.ts",
          editUrl:
            "https://github.com/LorenData/ecgrid-developer-documentation/tree/main/website/",
          // docItemComponent: "@theme/ApiItem",  // re-enable with openapi theme
        },
        blog: false,
        theme: {
          customCss: "./src/css/custom.css",
        },
      } satisfies Preset.Options,
    ],
  ],

  // themes: ["docusaurus-theme-openapi-docs"],  // re-enable after clean npm install

  themeConfig: {
    image: "img/ecgrid-social-card.png",
    colorMode: {
      defaultMode: "light",
      disableSwitch: false,
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: "Developer Portal",
      logo: {
        alt: "ECGrid",
        src: "img/ecgrid-network.svg",
        style: { height: "32px", width: "auto" },
      },
      items: [
        {
          type: "docSidebar",
          sidebarId: "gettingStartedSidebar",
          position: "left",
          label: "Getting Started",
        },
        {
          type: "docSidebar",
          sidebarId: "restApiSidebar",
          position: "left",
          label: "REST API",
        },
        {
          type: "docSidebar",
          sidebarId: "soapApiSidebar",
          position: "left",
          label: "SOAP API",
        },
        {
          type: "docSidebar",
          sidebarId: "commonOpsSidebar",
          position: "left",
          label: "Common Operations",
        },
        {
          type: "docSidebar",
          sidebarId: "samplesSidebar",
          position: "left",
          label: "Code Samples",
        },
          {
              href: "https://simplify.ecgrid.com/swagger/index.html",
              label: "Transformation API",
              position: "left",
          },
          {
              href: "https://globalproductaccess.com/swagger/index.html",
              label: "Data Sync and Catalog API",
              position: "left",
          },
        {
          href: "https://github.com/LorenData/ecgrid-developer-documentation",
          label: "GitHub",
          position: "right",
        },
      ],
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Documentation",
          items: [
            { label: "Getting Started", to: "/docs/getting-started/platform-overview" },
            { label: "REST API", to: "/docs/rest-api/overview" },
            { label: "SOAP API", to: "/docs/soap-api/overview" },
            {
              label: "Common Operations",
              to: "/docs/common-operations/overview",
            },
            { label: "Code Samples", to: "/docs/code-samples/overview" },
          ],
        },
        {
          title: "Live References",
            items: [
                {
                    label: "SOAP Web Service",
                    href: "https://os.ecgrid.io/v4.1/prod/ECGridOS.asmx",
                },
            {
              label: "REST Swagger UI",
              href: "https://rest.ecgrid.io/swagger/index.html",
            },
            {
              label: "Transformation Swagger UI",
              href: "https://simplify.ecgrid.com/swagger/index.html",
            },
            {
                label: "Data Sync and Catalog Swagger UI",
              href: "https://globalproductaccess.com/swagger/index.html",
            },
          ],
        },
        {
          title: "Support",
          items: [
            {
              label: "ECGrid.com",
              href: "https://ecgrid.com",
            },
            {
              label: "Support Portal",
              href: "https://ecgrid.freshdesk.com",
            },
            {
              label: "ECGrid Developer Documentation",
              href: "https://github.com/LorenData/ecgrid-developer-documentation",
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Loren Data Corp. All rights reserved.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ["csharp", "markup", "bash", "json"],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;

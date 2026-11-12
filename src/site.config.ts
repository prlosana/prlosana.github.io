import type {
  FooterConfig,
  LinkConfig,
  ProfileConfig,
  PublicationConfig,
  SiteConfig,
} from "@/types"

export const SITE: SiteConfig = {
  title: "Dr. Anasol Peña-Rios",
  description:
    "Distinguished Engineer & Researcher in Digital Twins, XR, AI, and Collaborative Environments.",
  href: "https://www.prlosana.com",
  author: "Dr. Anasol Peña-Rios",
  dir: "ltr",
  defaultPageImage: "/img/social-preview.png",
  defaultPostImage: "/img/social-preview.png",

  locale: {
    lang: "en-US",
    options: {
      day: "numeric",
      month: "short",
      year: "numeric",
      timeZone: "UTC",
    },
  },

  // Table of contents depth shared by blog posts and project detail pages.
  tocMaxDepth: 3,

  blog: {
    featuredPostCount: 3,
    postsPerPage: 8,
    shareActions: ["x", "linkedin"],
  },

  home: {
    careerHighlightCount: 4,
    updateCount: 3,
    publicationCount: 0,
  },

  favicon: "/favicon.ico",
  prerender: true,
  npmCDN: "https://cdn.jsdelivr.net/npm",

  license: {
    label: "CC-BY-4.0",
    href: "https://creativecommons.org/licenses/by/4.0/",
  },
}

export const PROFILE: ProfileConfig = {
  name: "Dr. Anasol Peña-Rios",
  tagline: "Distinguished Engineer & Research Technical Manager",
  email: "acpena@ieee.org",
  links: {
    email: "mailto:acpena@ieee.org",
    github: "https://github.com/prlosana",
    linkedin: "http://uk.linkedin.com/in/prlosana",
    googleScholar: "https://scholar.google.com/citations?user=6-UsGYsAAAAJ",
    orcid: "https://orcid.org/0000-0001-7109-9501",
    scopus: "https://www.scopus.com/authid/detail.uri?authorId=36835270200",
    researchgate: "https://www.researchgate.net/profile/Anasol-Pena-Rios",
  },
  highlightLinks: ["googleScholar", "linkedin", "github"],
  linksPlacement: {
    header: false,
    about: ["github", "linkedin", "googleScholar", "orcid", "scopus", "researchgate"],
    footer: ["email", "github", "linkedin", "googleScholar"],
  },
}

export const NAV_LINKS: LinkConfig[] = [
  { href: "/publications", label: "Publications" },
  { href: "/leadership", label: "Leadership" },
  { href: "/projects", label: "Projects" },
  { href: "/blog", label: "Posts" },
  { href: "/contact", label: "Contact" },
]

export const NAVIGATION: LinkConfig[] = NAV_LINKS.map(({ href, label }) => ({
  href,
  label,
}))

export const PUB_CONFIG: PublicationConfig = {
  maxFirstAuthors: 6,
  maxLastAuthors: 1,
  highlightAuthor: {
    firstName: "Anasol",
    lastName: "Peña-Rios",
    aliases: [
      "A. Peña-Rios",
      "A. Pena-Rios",
      "Anasol Pena-Rios",
      "A. C. Peña-Rios",
      "A. C. Pena-Rios",
      "Peña-Rios, A.",
      "Pena-Rios, A.",
      "Peña Rios, A.",
    ],
  },
  equalSymbols: {
    first: "*",
    second: "†",
    third: "‡",
    last: "§",
  },
}

export const FOOTER: FooterConfig = {
  credits: false,
  footerLinks: [],
}

if (import.meta.env.DEV && typeof window === "undefined") {
  const {
    FooterConfigSchema,
    ProfileConfigSchema,
    PublicationConfigSchema,
    SiteConfigSchema,
  } = await import("@/schemas")
  SiteConfigSchema.parse(SITE)
  ProfileConfigSchema.parse(PROFILE)
  FooterConfigSchema.parse(FOOTER)
  PublicationConfigSchema.parse(PUB_CONFIG)
}

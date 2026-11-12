# Dr. Anasol Peña-Rios - Academic Website (Astro + MyScholar)

This repository contains the source code for the personal and academic website of **Dr. Anasol Peña-Rios** ([www.prlosana.com](https://www.prlosana.com/)), migrated to **[Astro](https://astro.build/)** using the **[MyScholar](https://github.com/mychiffonn/myscholar)** theme.

---

## 📊 Overview & Tech Stack

* **Framework**: [Astro](https://astro.build/) v7 (Static site generation)
* **Theme**: [MyScholar](https://github.com/mychiffonn/myscholar) (Academic portfolio, BibTeX citations, Markdown-first)
* **Publications Engine**: `@citation-js/core` parsing `src/content/publications/main.bib` (102 peer-reviewed publications, patents, proceedings, books, and theses with author highlighting and one-click "Copy BibTeX")
* **Styling**: Native CSS tokens, light/dark mode switching, responsive typography
* **Analytics**: Google Analytics 4 (`GT-MK4N6BD`)
* **Deployment**: GitHub Pages configured to serve from `docs/` with custom domain `www.prlosana.com`

---

## 🚀 Quick Start

### Prerequisites
* **Node.js**: `>= 22.12.0` (Node 26 recommended)
* **Package Manager**: `pnpm`

### Local Development

1. Install dependencies:
   ```bash
   pnpm install
   ```

2. Start the local development server:
   ```bash
   pnpm dev
   ```
   Open [http://localhost:4321](http://localhost:4321) in your browser.

3. Type and lint checks:
   ```bash
   pnpm check
   ```

4. Build for production (outputs to `docs/`):
   ```bash
   pnpm build
   ```

---

## 📁 Project Structure

```
├── astro.config.ts             # Astro configuration (static output, docs/ outDir, sitemap, Goldmark/Sätteri)
├── src/
│   ├── site.config.ts          # Profile, navigation, metadata, and publication author highlighting
│   ├── content/
│   │   ├── publications/
│   │   │   └── main.bib        # All 102 publications in structured BibTeX format
│   │   ├── projects/           # Project markdown files (Research, Tools, KTP)
│   │   ├── blog/               # Research blog posts & news articles
│   │   ├── updates/            # Recent news highlights and awards
│   │   ├── experience.json     # Academic & industry career history
│   │   ├── people.toml         # Author profiles
│   │   ├── about.md            # Homepage biography
│   │   ├── misc.md             # Research focus areas
│   │   └── services.md         # Collaboration & service areas
│   ├── pages/
│   │   ├── index.astro         # Homepage
│   │   ├── publications.astro  # BibTeX publications list with search and year/relevance sort
│   │   ├── leadership.astro    # Leadership, awards & service with interactive tabs
│   │   ├── projects/           # Projects catalog and detail pages
│   │   ├── blog/               # Blog index and post readers
│   │   └── contact.astro       # Contact information & academic profiles
│   ├── layouts/                # Astro layouts
│   ├── components/             # Reusable UI components
│   └── styles/                 # Theme CSS
├── public/                     # Static assets (images, fonts, favicon, CNAME)
├── docs/                       # Static build output deployed to GitHub Pages
└── hugo-legacy/                # Archived Hugo source files for reference
```

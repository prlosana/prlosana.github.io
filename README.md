# Dr. Anasol Peña-Rios - Academic Website

This is the Hugo-based personal and academic portfolio website for **Dr. Anasol Peña-Rios**, built with Hugo (Extended), the PaperMod theme, Material Design 3 design enhancements, and an automated BibLaTeX publications pipeline.

---

## 📊 Site Overview

- **Static Site Generator**: [Hugo](https://gohugo.io/) (Extended)
- **Theme**: [PaperMod](https://github.com/adityatelange/hugo-PaperMod) with Material Design 3 styling
- **Hosting / Deployment**: GitHub Pages (served directly from the `/docs` directory on branch `main`)
- **Package Management**: `pnpm`
- **Publications Engine**: BibLaTeX (`static/publications.bib`) compiled via Python to multi-style JSON citations
- **Navigation Structure**:
  - **About Me (`/`)**: Professional biography, research highlights, and integrated Contact section
  - **Publications (`/publications/`)**: Interactive list with multi-style citations (APA, IEEE, Harvard, ACM, Chicago, MLA), category filtering, search, and patent status chips
  - **Leadership & Service (`/leadership/`)**: Interactive tabbed view of leadership roles, honours, awards, and community service
  - **Projects (`/projects/`)**: Research initiatives, PhD work, and consolidated Posts section with compact card summaries
  - **Search (`/search/`)**: Real-time client-side search powered by Fuse.js
  - **Art (`/art/`)**: Creative works and artistic portfolio

---

## 🚀 Quick Start

### Prerequisites

1. **Hugo Extended** (v0.120+ recommended)
   - macOS: `brew install hugo`
2. **Node.js & pnpm**
   - Node.js (v18+)
   - `corepack enable` or `npm install -g pnpm`
3. **Python 3** (for the publications pipeline)
   - Standard Python 3.8+ (no external pip dependencies required)

### Local Development

1. **Clone and navigate to the directory**:
   ```bash
   git clone https://github.com/prlosana/prlosana-hugo.git
   cd prlosana-hugo
   ```

2. **Start the local development server**:
   ```bash
   pnpm dev
   ```
   *(This automatically compiles `static/publications.bib` and starts Hugo server with drafts enabled).*

3. **View the site**:
   Open [http://localhost:1313](http://localhost:1313) in your browser. All menu links use site-relative paths so browsing works locally without redirecting to the live domain.

---

## 🛠️ Build & Deployment

### Building for Production

GitHub Pages serves the compiled website directly from the `/docs` directory.

To build the complete website for production:
```bash
pnpm build
```
This runs:
1. `python3 scripts/build_publications.py` to compile `static/publications.bib` into `data/publications.json`.
2. `hugo --minify` to generate the static files into `docs/`.

### Deployment to GitHub Pages

1. Build the production files:
   ```bash
   pnpm build
   ```
2. Commit and push changes:
   ```bash
   git add -A
   git commit -m "Deploy update"
   git push origin main
   ```
3. GitHub Pages is configured in repo settings:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/docs`

---

## 📚 Managing Publications (`publications.bib`)

The single source of truth for all publications is [`static/publications.bib`](static/publications.bib).

### 1. Adding or Editing Entries

Simply open `static/publications.bib` in your editor and add standard BibLaTeX entries (`@article`, `@inproceedings`, `@book`, `@incollection`, `@patent`, etc.).

#### Example: Regular Publication
```biblatex
@article{penarios2024collaborative,
  author    = {Peña-Rios, Anasol and Callaghan, Victor and Gardner, Michael},
  title     = {Collaborative Learning in Mixed Reality Environments},
  journal   = {IEEE Transactions on Learning Technologies},
  year      = {2024},
  volume    = {17},
  number    = {2},
  pages     = {120--134},
  doi       = {10.1109/TLT.2024.1234567}
}
```

#### Example: Patents & Patent Applications
The publications page automatically renders patent status chips (`Granted Patent` vs `Patent Application`) and displays patent notes:
```biblatex
@patent{penarios2024fieldforce,
  author    = {Peña-Rios, Anasol and Hagras, Hani and Owusu, Gilbert},
  title     = {System and Method for Intelligent Workforce Scheduling in Mixed Reality},
  type      = {patent},
  number    = {US 11,234,567 B2},
  date      = {2024-05-14},
  year      = {2024},
  holder    = {British Telecommunications plc},
  doi       = {10.1234/patent.567},
  note      = {Granted patent covering distributed AI algorithms for enterprise workforce optimization.}
}
```
* **Patent Type**:
  - `type = {patent}`: Renders as **Granted Patent** (green chip)
  - `type = {patentapp}` or `type = {patentus}`: Renders as **Patent Application** (blue chip)
* **Patent Note**: Text in `note = {...}` is rendered in an informational note box directly below the citation.

### 2. Compiling the Publications List

Whenever you edit `static/publications.bib`, run:
```bash
pnpm bib
```
or rebuild the entire site with `pnpm build`.

The script parses BibLaTeX entries and generates ready-to-render citations across six standard citation formats:
- **APA** (default)
- **IEEE**
- **Harvard**
- **ACM**
- **Chicago**
- **MLA**

Users can interactively switch citation formats on the Publications page using the format dropdown selector.

---

## 📁 Project Structure

```
prlosana-hugo/
├── assets/                 # Custom asset pipeline
│   └── css/extended/
│       └── material3.css   # Material Design 3 theme extensions & chips
├── content/                # Content markdown files
│   ├── _index.md           # About Me (Home) page with integrated Contact section
│   ├── art.md              # Art page content
│   ├── leadership.md       # Leadership & Service content
│   ├── projects.md         # Projects page content
│   ├── publications.md     # Publications page entrypoint
│   ├── search.md           # Search page entrypoint
│   └── posts/              # Published & historical blog posts
├── data/
│   └── publications.json   # Generated multi-style publications dataset
├── docs/                   # Production build directory (served by GitHub Pages)
├── layouts/                # Hugo template overrides
│   ├── _default/
│   │   ├── baseof.html     # Base HTML layout
│   │   ├── projects.html   # Projects page layout with consolidated Posts section
│   │   └── publications.html # Interactive BibLaTeX publications page layout
│   └── partials/           # Header, footer, and menu partials
├── scripts/
│   └── build_publications.py # BibLaTeX parser & citation generator
├── static/                 # Static assets copied directly to docs/
│   ├── images/             # Images and figures
│   └── publications.bib    # Source of truth BibLaTeX file
├── themes/
│   └── PaperMod/           # Submodule/vendor PaperMod theme
├── hugo.toml               # Hugo site configuration
├── package.json            # NPM scripts & metadata
└── README.md               # Project documentation
```

---

## 🎨 Design & Customizations

1. **Integrated Contact Section**:
   - The contact page was consolidated directly into the bottom of the Home page ([`content/_index.md`](content/_index.md)).
   - Features social profile links (GitHub, LinkedIn, ResearchGate, Google Scholar), email, and contact info without requiring a separate page.

2. **Consolidated Projects & Posts**:
   - Blog posts are consolidated at the bottom of the Projects page ([`content/projects.md`](content/projects.md) / [`layouts/_default/projects.html`](layouts/_default/projects.html)).
   - Post cards feature compact summary teasers (`line-clamp: 3`), clean titles, and fully uncropped thumbnails (`object-fit: contain; max-height: 115px;`).

3. **Material Design 3 Styling**:
   - Surface elevation, assist chips, and pill filters.
   - Full dark/light mode compatibility.
   - Clean DOI buttons with raw URLs stripped in favor of interactive chips.

4. **Standards Compatibility**:
   - Modern CSS standards compliant (`line-clamp` paired with `-webkit-line-clamp`).
   - Clean mobile-responsive layouts across all breakpoints.

---

## 🔧 Useful Scripts Reference

| Command | Action |
|---|---|
| `pnpm dev` | Compile publications + run local development server with live reload |
| `pnpm build` | Compile publications + build production static site to `docs/` |
| `pnpm bib` | Compile `static/publications.bib` into `data/publications.json` |
| `hugo server -D` | Run Hugo development server directly |
| `hugo --minify` | Run Hugo build directly |

---

## 📄 License

Content © Dr. Anasol Peña-Rios. Code and templates licensed under the [MIT License](LICENSE).

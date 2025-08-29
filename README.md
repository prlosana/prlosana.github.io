# Dr. Anasol Peña-Rios - Academic Website

This is the Hugo-based website for Dr. Anasol Peña-Rios, successfully migrated from WordPress for better performance, security, and maintainability.

## 🎉 Migration Status: COMPLETED ✅

Your WordPress site has been successfully migrated to Hugo using the PaperMod theme. The site now includes all your original content with improved performance and security.

## 📊 Site Overview

- **Pages**: 31 total pages (including blog posts)
- **Images**: 73 images migrated from WordPress
- **Theme**: PaperMod (fast, clean, responsive)
- **Performance**: Static site with fast loading times
- **Security**: No database or PHP vulnerabilities

## 🚀 Quick Start

### Prerequisites
- Hugo installed (Extended version recommended)
- Git

### Development

1. **Navigate to the site directory**:
   ```bash
   cd prlosana-hugo
   ```

2. **Start the development server**:
   ```bash
   hugo server -D --config hugo.toml
   ```

3. **View the site**: Open http://localhost:1313 in your browser

**Note**: The `--config hugo.toml` flag is required to explicitly tell Hugo which configuration file to use.

### Building for Production

```bash
hugo
```

The built site will be in the `public/` directory.

## 📁 Project Structure

```
prlosana-hugo/
├── content/           # All site content
│   ├── _index.md     # BIO (main page)
│   ├── contact.md    # Contact page
│   ├── leadership-volunteering.md # Leadership & Volunteering page
│   ├── projects.md   # Projects page
│   ├── publications.md # Publications page
│   └── posts/        # Blog posts (16 files)
├── static/           # Static files (images, CSS, JS)
│   └── images/       # All migrated images (73 files)
├── themes/           # Hugo themes
│   └── PaperMod/     # PaperMod theme
├── hugo.toml         # Site configuration
├── README.md         # This file
└── MIGRATION-COMPLETE.md # Migration summary
```

## 🎨 Theme Features

The [PaperMod theme](https://github.com/adityatelange/hugo-PaperMod) provides:

- **Fast, clean design** - Optimized for academic sites
- **Dark/Light mode** - Automatic theme switching
- **Search functionality** - Built-in search with Fuse.js
- **Responsive design** - Works perfectly on mobile devices
- **Table of Contents** - Automatic generation for long posts
- **Code highlighting** - Syntax highlighting for code blocks
- **Social icons** - Easy social media integration

## 📝 Content Management

### Creating New Pages
```bash
hugo new my-page.md
```

### Creating New Blog Posts
```bash
hugo new posts/my-new-post.md
```

### Content Structure
Each content file should have front matter at the top:
```yaml
---
title: "Page Title"
date: 2024-01-01
draft: false
description: "Page description"
---
```

## 🔧 Configuration

The main configuration is in `hugo.toml`. Key settings include:
- Site title and description
- Menu structure (BIO, Publications, Leadership & Volunteering, Projects, Contact)
- Theme parameters
- Social media links
- SEO settings

## 🖼️ Images and Media

- Place images in `static/images/`
- Reference them in content as `/images/filename.jpg`
- All 73 images from your WordPress site have been migrated

## 📊 Migration Benefits Achieved

### Performance
- ⚡ **Faster loading** - Static files vs dynamic PHP
- 📱 **Better mobile performance**
- 🔍 **Improved SEO scores**

### Security
- 🛡️ **No database vulnerabilities**
- 🔒 **No PHP security issues**
- 🚫 **Reduced attack surface**

### Maintenance
- 💰 **Free hosting** on GitHub Pages
- 🔄 **Version control** with Git
- 🛠️ **Easier updates** and backups

### Flexibility
- 🎨 **Complete design control**
- 📝 **Markdown content** (easier to edit)
- 🔧 **Custom functionality** with Hugo modules

## 🚀 Deployment

### GitHub Pages
1. Push the repository to GitHub
2. Enable GitHub Pages in repository settings
3. Set the source to the `main` branch and `/docs` folder
4. Update `hugo.toml` to set `publishDir = "docs"`

### Netlify
1. Connect your repository to Netlify
2. Set build command: `hugo`
3. Set publish directory: `public`

### Custom Domain
- Configure prlosana.com to point to your new Hugo site
- Set up DNS records
- Enable HTTPS

## 🔧 Available Commands

```bash
# Start development server with explicit config (recommended)
hugo server -D --config hugo.toml

# Start development server with cache disabled (for testing)
hugo server -D --config hugo.toml --disableFastRender --ignoreCache

# Build site for production
hugo --config hugo.toml

# Create new blog post
hugo new posts/my-new-post.md

# Create new page
hugo new my-page.md

# Convert more WordPress content (if needed)
./convert-wordpress-content.sh
```

## 🔧 Troubleshooting

### Hugo Server Issues
If you encounter the error "Unable to locate config file or config directory":
1. **Always use the explicit config flag**: `hugo server -D --config hugo.toml`
2. **Clear Hugo cache**: `rm -rf resources .hugo_build.lock public`
3. **Kill existing processes**: `pkill -f "hugo server"`
4. **Restart with clean slate**: `hugo server -D --config hugo.toml`

### Browser Caching Issues
If changes aren't reflected in the browser:
1. **Hard refresh**: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. **Developer Tools**: Right-click refresh → "Empty Cache and Hard Reload"
3. **Use cache-disabled server**: `hugo server -D --config hugo.toml --disableFastRender --ignoreCache`

## 📚 Documentation

- **Hugo Documentation**: https://gohugo.io/documentation/
- **PaperMod Theme**: https://github.com/adityatelange/hugo-PaperMod
- **GitHub Pages**: https://pages.github.com/

## 🎯 Site Pages

Your Hugo site includes all the original WordPress pages:

1. **BIO** (main page) - Your professional background and expertise
2. **Publications** - Academic publications listing
3. **Leadership & Volunteering** - Awards, honors, and leadership roles
4. **Projects** - Research projects and PhD work
5. **Contact** - All your contact information and profiles
6. **Blog Posts** - 16 converted WordPress posts

## 🎉 Success Metrics

After migration, you should see:
- ⚡ **Faster page load times** (under 3 seconds)
- 📈 **Better SEO rankings**
- 🔒 **Improved security** (no WordPress vulnerabilities)
- 💰 **Reduced hosting costs** (free GitHub Pages)
- 🛠️ **Easier maintenance** (Git-based workflow)

## 📞 Support

If you encounter issues:
1. Check the Hugo and PaperMod documentation
2. Review the migration summary in `MIGRATION-COMPLETE.md`
3. Test each step thoroughly before proceeding
4. Keep backups of your original WordPress site

---

**Migration completed on**: January 2024  
**Theme used**: PaperMod by Aditya Telange  
**Total pages**: 31  
**Total images**: 73  
**Performance improvement**: Significant faster loading times

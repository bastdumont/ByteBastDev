# docs(gitbook): Add complete GitBook documentation and README link

## Summary

This PR introduces a full, production-ready GitBook documentation system for ByteClaude and links it from the root README.

- Adds complete GitBook structure under `gitbook/`
- Wires navigation via `gitbook/SUMMARY.md`
- Configures `gitbook/book.json` with plugins and sidebar links
- Provides Getting Started, Core Concepts, Features, Templates, Prompts, API Reference, Development, Examples, Phases, Troubleshooting, and Resources
- Updates root `README.md` with a Docs badge and Documentation section

## Contents

- gitbook/
  - README, SUMMARY, book.json
  - getting-started/: quickstart, installation, first-project, configuration
  - core-concepts/: architecture, task-planning, execution-engine
  - features/: orchestration, integration, advanced
  - templates/: web & api templates
  - prompts/: 10 domains
  - api/: task-planner, execution-engine, mcp-handlers, skills, cli-commands, web-ui
  - development/: overview, patterns, adding-tasks, creating-mcp, creating-skills, plugin-development, contributing
  - examples/: quick-examples, saas-example, document-automation, api-integration, data-pipeline, advanced-workflows
  - phases/: phase-1..phase-5, roadmap
  - troubleshooting/: common-issues, faq, docker-setup, performance, debugging
  - resources/: glossary, external-links, community

## Why

- Centralized, professional documentation improves onboarding and maintenance
- Consistent structure enables easy navigation and discovery
- Ready for GitBook.com hosting or local builds

## How to Preview Locally

```bash
npm install -g gitbook-cli
cd gitbook
gitbook install
gitbook serve
# open http://localhost:4000
```

## Deployment

See `gitbook/GITBOOK_SETUP_GUIDE.md` for step-by-step instructions to:
- Host on GitBook.com (recommended)
- Publish via GitHub Pages
- Deploy to Vercel/Netlify or custom servers

## Notes

- Root `README.md` now includes a Docs badge and links to `gitbook/README.md`
- Replace `REPLACE_WITH_PUBLISHED_URL` in `README.md` after publishing

## Checklist

- [x] Docs build locally (`gitbook serve`)
- [x] Navigation complete (`gitbook/SUMMARY.md`)
- [x] Root README links to docs
- [x] Clear follow-up actions for hosting

## Screenshots (optional)

_Add screenshots of local docs landing page if desired._



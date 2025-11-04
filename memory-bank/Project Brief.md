# Project Brief

## Project Name
**ByteClaude** (originally "Automated Development Framework")

## Core Requirements

### Primary Goal
Build an automated software development framework that converts natural language requests into fully functional, production-ready applications through intelligent orchestration of Claude Code, Skills, MCPs (Model Context Protocol), and Context7 documentation.

### Key Objectives

1. **Natural Language to Software**
   - Accept natural language task descriptions
   - Intelligently decompose into structured execution plans
   - Generate complete, working applications

2. **Intelligent Orchestration**
   - Automatic technology detection (React, Next.js, MongoDB, Stripe, etc.)
   - Dependency resolution and parallel execution optimization
   - Context-aware development with real-time documentation

3. **Multi-Platform Integration**
   - 15+ MCP integrations (MongoDB, Stripe, Notion, Airtable, HubSpot, etc.)
   - 10+ Skills (docx, pdf, pptx, xlsx, artifacts-builder, theme-factory, etc.)
   - Context7 for dynamic library documentation retrieval

4. **Production Quality**
   - Automated testing generation
   - Code validation and security scanning
   - Comprehensive documentation generation
   - Best practices enforcement

## Scope

### In Scope

**Core Framework:**
- Task planning and decomposition engine
- Execution orchestration with parallel processing
- MCP handler layer (8 handlers implemented)
- Skill adapter layer (4 adapters implemented)
- Context7 integration client
- Configuration management system
- File management utilities
- Validation and security scanning
- Template engine for code generation
- Expert prompt builder

**Project Templates:**
- 7 production-ready boilerplates (47% complete)
  - Next.js SaaS application
  - React Dashboard
  - FastAPI Backend
  - Express.js API
  - Python CLI Tool
  - Chrome Extension
  - Vue.js SPA

**Documentation:**
- Comprehensive README and architecture docs
- Getting started guides
- Implementation status tracking
- Project templates documentation

### Out of Scope (Current Phase)

- Visual workflow designer (Phase 5)
- Real-time monitoring dashboard (Phase 5)
- Web UI interface (Phase 5)
- Cloud deployment automation (Phase 7)
- CI/CD pipeline templates (Phase 7)

## Target Users

1. **Developers** - Build applications faster with natural language
2. **Teams** - Standardize project initialization and best practices
3. **Startups** - Rapid MVP development with integrated services
4. **Agencies** - Consistent project scaffolding across clients

## Success Criteria

1. ✅ Framework successfully converts natural language to working code
2. ✅ Supports major web frameworks (React, Next.js, Vue, FastAPI, Express)
3. ✅ Integrates with 15+ external services via MCPs
4. ✅ Generates production-ready boilerplates (7/15 complete)
5. ✅ Provides comprehensive documentation and examples
6. ⏳ Complete test coverage (Phase 6)
7. ⏳ Full boilerplate library (15 templates - 47% complete)

## Constraints

- **Skills Location**: `/mnt/skills/` (public and examples subdirectories)
- **Docker Requirement**: MongoDB, Stripe, Notion, YouTube MCPs require Docker
- **Python Version**: 3.8+ required
- **Async Pattern**: All handlers use async/await pattern
- **Configuration**: YAML-based configuration system

## Architecture Principles

1. **Modularity**: Clear separation between planning, execution, and integrations
2. **Extensibility**: Easy to add new MCPs, Skills, and templates
3. **Type Safety**: Comprehensive type hints throughout codebase
4. **Error Handling**: Graceful degradation with retry logic
5. **Performance**: Parallel execution with dependency optimization
6. **Documentation**: Self-documenting code with comprehensive docs


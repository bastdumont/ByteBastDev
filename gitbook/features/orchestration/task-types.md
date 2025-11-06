# Task Types

Framework-supported task categories used by the planner and execution engine.

## Available Types

- FILE_OPERATION: project setup, file creation/moves
- CODE_GENERATION: source code generation and refactoring
- WEB_DEVELOPMENT: UI projects and web artifacts
- DOCUMENT_GENERATION: pdf, docx, pptx, xlsx
- API_INTEGRATION: MCP-driven external integrations
- DATABASE_OPERATION: database reads/writes, schema ops
- TESTING: unit/integration tests and coverage
- VALIDATION: linting, static checks, documentation
- DATA_PROCESSING: ETL and batch transforms
- DEPLOYMENT: packaging, containerization, releases

## Usage

The planner assigns types automatically based on your request. Types determine handler selection, validation, and reporting buckets.



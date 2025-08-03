# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based agent that automatically generates unit tests for Python/TypeScript files using LangGraph, LLMs, and GitHub. The agent creates PRs with generated tests and iterates based on PR comments.

## Development Environment

The project uses Poetry for dependency management and virtual environments.

### Essential Commands

```bash
# Install dependencies
poetry install

# Run the main agent
poetry run python agent/main.py

# Run tests  
poetry run pytest

# Run linting
poetry run ruff check

# Format code
poetry run ruff format

# Install pre-commit hooks
poetry run pre-commit install
```

## Code Architecture

- **`agent/`** - Main agent implementation
  - `main.py` - Entry point with basic hello world functionality
  - `workflows/` - Directory for LangGraph workflow definitions (currently empty)
- **`src/`** - Source code that the agent will analyze and generate tests for
  - `example.py` - Simple example functions (add_numbers, greet) 
- **`test/`** - Test directory (currently empty, will be populated by the agent)

## Key Dependencies

- **LangGraph** (0.6.x) - Workflow orchestration for the test generation agent
- **LangChain** (0.3.x) - LLM integration and tooling
- **pytest** - Testing framework for generated tests
- **pydantic** - Data validation and models
- **ruff** - Fast Python linter and formatter

The project is configured to use Poetry for all dependency management, and includes pre-commit hooks for code quality.
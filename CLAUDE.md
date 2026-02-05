# CLAUDE.md

This file provides guidance for AI assistants working with this repository.

## Repository Overview

**Debug** is a debug and testing repository (调试代码，测试代码功能). It serves as a sandbox environment for testing code functionality and debugging experiments.

## Project Structure

```
Debug/
├── CLAUDE.md      # AI assistant guidance (this file)
└── README.md      # Project description
```

This is a minimal repository that can be extended with code, tests, and configurations as needed.

## Development Workflow

### Getting Started

1. Clone the repository
2. Create a feature branch for your work
3. Add your debug/test code
4. Commit with clear, descriptive messages
5. Push changes to your branch

### Branch Naming Convention

- Feature branches: `feature/<description>`
- Debug branches: `debug/<description>`
- Test branches: `test/<description>`
- Claude AI branches: `claude/<session-id>`

### Commit Message Guidelines

Write clear, concise commit messages that describe what changed and why:

- Use imperative mood: "Add feature" not "Added feature"
- Keep the first line under 72 characters
- Add details in the body if needed

Examples:
```
Add unit tests for parsing module
Fix edge case in data validation
Refactor authentication flow for clarity
```

## Code Conventions

Since this is a testing/debug repository, it may contain code in various languages. Follow these general principles:

### General Guidelines

- Write clear, readable code with meaningful variable names
- Add comments for complex logic
- Keep functions focused and small
- Handle errors appropriately
- Remove debug code before committing to main branches

### When Adding New Code

1. Create appropriate directory structure (e.g., `src/`, `tests/`, `scripts/`)
2. Add relevant configuration files for the language/framework used
3. Update this CLAUDE.md with language-specific conventions if needed
4. Add a `.gitignore` for generated/temporary files

## Testing

When adding tests to this repository:

1. Place test files in a `tests/` or `__tests__/` directory
2. Name test files clearly (e.g., `test_<module>.py`, `<module>.test.js`)
3. Write descriptive test names that explain what is being tested
4. Include both positive and negative test cases

## AI Assistant Guidelines

When working in this repository as an AI assistant:

### Do

- Read existing files before making changes
- Follow any existing code patterns and conventions
- Make focused, incremental changes
- Explain your reasoning for significant changes
- Test code changes when possible
- Create meaningful commit messages

### Don't

- Overwrite files without understanding their content
- Add unnecessary complexity
- Leave debug artifacts (console.log, print statements) in final code
- Make changes outside the scope of the request
- Commit sensitive information (API keys, credentials)

### File Operations

- Always read a file before editing it
- Prefer editing over creating new files when appropriate
- Keep files focused on a single purpose
- Use consistent formatting within files

## Future Enhancements

As this repository grows, consider adding:

- [ ] `.gitignore` for common temporary/generated files
- [ ] CI/CD configuration (GitHub Actions, etc.)
- [ ] Code formatting configuration (Prettier, Black, etc.)
- [ ] Linting rules (ESLint, Pylint, etc.)
- [ ] Pre-commit hooks for code quality
- [ ] Detailed documentation for specific modules

---

*Last updated: 2026-02-05*

# Contributing to BitNet LLM Virtual Co-worker Builder

Thank you for your interest in contributing to BitNet LLM Virtual Co-worker Builder! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to foster an inclusive and respectful community.

## How to Contribute

There are many ways to contribute to the project:

1. **Report bugs**: If you find a bug, please create an issue with a detailed description of the problem, steps to reproduce, and your environment.
2. **Suggest features**: If you have an idea for a new feature or improvement, please create an issue to discuss it.
3. **Improve documentation**: Help us improve the documentation by fixing typos, adding examples, or clarifying explanations.
4. **Submit code changes**: Fix bugs, add features, or improve the codebase by submitting pull requests.

## Development Setup

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/BitNet-LLM-Virtual-Coworker-Builder.git
   cd BitNet-LLM-Virtual-Coworker-Builder
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```
4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes and write tests if applicable.
3. Run the tests to ensure everything is working:
   ```bash
   pytest
   ```
4. Format your code:
   ```bash
   black src tests
   isort src tests
   ```
5. Commit your changes with a descriptive commit message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```
6. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. Create a pull request on GitHub.

## Pull Request Guidelines

- Follow the coding style and conventions used in the project.
- Include tests for new features or bug fixes.
- Update documentation if necessary.
- Keep pull requests focused on a single change or feature.
- Write a clear and descriptive title and description for your pull request.

## Code Style

We use the following tools to maintain code quality:

- **Black**: For code formatting
- **isort**: For import sorting
- **flake8**: For linting
- **mypy**: For type checking

You can run all of these tools with:

```bash
black src tests
isort src tests
flake8 src tests
mypy src
```

## Testing

We use pytest for testing. To run the tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=bitnet_vc_builder
```

## Documentation

We use Markdown for documentation. Please update the documentation when you make changes to the codebase.

## Production Setup

If you're working on features related to the production deployment of BitNet LLM Virtual Co-worker Builder, please follow these guidelines:

1. Test all production-related changes thoroughly before submitting a pull request.
2. Update the `PRODUCTION_SETUP.md` file with any changes to the production setup process.
3. Ensure that all production scripts are compatible with the target operating systems (primarily Windows).
4. Add appropriate error handling and logging to production scripts.
5. Document any new environment variables or configuration options.

For more information on the production setup, see the [Production Setup Guide](PRODUCTION_SETUP.md).

## Monitoring and Backup

If you're working on features related to monitoring or backup:

1. Ensure that monitoring scripts provide clear and actionable information.
2. Test backup and restore functionality thoroughly.
3. Document any changes to the monitoring or backup systems.
4. Consider security implications of any changes to these systems.

## License

By contributing to BitNet LLM Virtual Co-worker Builder, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

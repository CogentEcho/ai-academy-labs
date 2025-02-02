# Deployment Workflow

## GitHub Actions Workflow
_Location: .github/workflows/deploy.yml_

```yaml
name: Deploy AI Academy Labs

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Run tests
        run: |
          python -m pytest tests/
          
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Lint Markdown
        uses: avto-dev/markdown-lint@v1
        with:
          config: '.markdownlint.json'
          args: '**/*.md'
          
      - name: Lint Python
        run: |
          pip install flake8
          flake8 .
          
  build-and-deploy:
    needs: [test, lint]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '14'
          
      - name: Install dependencies
        run: |
          npm install
          
      - name: Build site
        run: |
          npm run build
          
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist

  update-notebooks:
    needs: [test]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Update Colab notebooks
        run: |
          python scripts/update_notebooks.py
          
      - name: Commit updates
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add notebooks/
          git commit -m "Update notebooks" || echo "No changes to commit"
          git push
```

## Local Development Setup
_Location: scripts/setup_local.sh_

```bash
#!/bin/bash

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Setup local configuration
cp config/local.example.yml config/local.yml

# Initialize git submodules (if any)
git submodule update --init --recursive

echo "Local development environment setup complete!"
```

## Deployment Documentation
_Location: docs/deployment.md_

```markdown
# Deployment Guide

## Prerequisites
- GitHub account with repository access
- Python 3.9+
- Node.js 14+
- Git

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/cogentecho/ai-academy-labs.git
   cd ai-academy-labs
   ```

2. Run setup script:
   ```bash
   ./scripts/setup_local.sh
   ```

3. Start local development server:
   ```bash
   npm run dev
   ```

## Deployment Process

### Automatic Deployment
1. Push changes to main branch
2. GitHub Actions will:
   - Run tests
   - Lint code
   - Build site
   - Deploy to GitHub Pages
   - Update Colab notebooks

### Manual Deployment
```bash
# Build
npm run build

# Deploy
npm run deploy
```

## Monitoring

1. Check GitHub Actions status
2. Verify deployed site
3. Test Colab notebook links
4. Review access logs

## Rollback Procedure

1. Find last working commit
2. Reset main branch:
   ```bash
   git reset --hard <commit-hash>
   git push -f origin main
   ```

3. Monitor deployment

## Maintenance

### Daily
- Check access logs
- Verify Colab notebooks accessibility

### Weekly
- Run full test suite
- Update dependencies
- Review security alerts

### Monthly
- Full content review
- Update documentation
- Performance optimization
```

## Testing Setup
_Location: tests/conftest.py_

```python
import pytest
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def test_data():
    """Provide test data for unit tests"""
    return {
        'sample_lesson': 'tests/data/sample_lesson.md',
        'sample_notebook': 'tests/data/sample_notebook.ipynb'
    }

@pytest.fixture
def test_config():
    """Provide test configuration"""
    return {
        'base_url': 'http://localhost:3000',
        'github_pages_url': 'https://cogentecho.ai/ai-academy-labs'
    }
```

## Configuration Files
_Location: config/default.yml_

```yaml
site:
  title: AI Academy Labs
  description: Learn AI from First Principles
  base_url: https://cogentecho.ai/ai-academy-labs

github:
  repo: cogentecho/ai-academy-labs
  branch: main

colab:
  base_url: https://colab.research.google.com/github/cogentecho/ai-academy-labs/blob/main/notebooks

build:
  output_dir: dist
  assets_dir: assets
  notebooks_dir: notebooks
```

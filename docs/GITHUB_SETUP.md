# GitHub Setup Guide for TinyLLM-Auto

This guide will walk you through setting up the TinyLLM-Auto project on GitHub.

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the "+" icon in the top right and select "New repository"
3. Fill in the details:
   - **Repository name**: `tinyllm-auto`
   - **Description**: "Edge LLM for In-Vehicle Deployment - Optimized small language model for automotive conversational AI"
   - **Visibility**: Public (or Private if you prefer)
   - **DO NOT** initialize with README (we already have one)
4. Click "Create repository"

## Step 2: Initialize Local Git Repository

Open your terminal in the project directory and run:

```bash
# Navigate to project directory
cd tinyllm-auto

# Initialize git repository
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: TinyLLM-Auto project setup"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/sreekar-gajula/tinyllm-auto.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Set Up GitHub Repository Settings

### Add Topics/Tags
Go to your repository on GitHub and add these topics:
- `automotive`
- `llm`
- `edge-computing`
- `conversational-ai`
- `vehicle-diagnostics`
- `phi-2`
- `llama-cpp`
- `raspberry-pi`

### Enable GitHub Actions
GitHub Actions should be automatically enabled. Verify by going to the "Actions" tab.

### Set Up Branch Protection (Optional but Recommended)
1. Go to Settings → Branches
2. Add rule for `main` branch:
   - ✓ Require pull request reviews before merging
   - ✓ Require status checks to pass before merging
   - ✓ Include administrators (optional)

## Step 4: Add Repository Secrets (for CI/CD)

If you plan to use any external services:
1. Go to Settings → Secrets and variables → Actions
2. Add secrets as needed (e.g., API keys, deployment credentials)

## Step 5: Create GitHub Releases

### Creating Your First Release

```bash
# Tag your first release
git tag -a v0.1.0 -m "Initial release: Basic automotive assistant functionality"
git push origin v0.1.0
```

Then on GitHub:
1. Go to Releases → Create a new release
2. Choose tag: `v0.1.0`
3. Release title: `v0.1.0 - Initial Release`
4. Description:
```markdown
## 🎉 Initial Release

TinyLLM-Auto v0.1.0 - Edge LLM for In-Vehicle Deployment

### Features
- ✅ Phi-2 (2.7B) with 4-bit GGML quantization
- ✅ CPU-only inference (<8GB RAM)
- ✅ Voice interface (Whisper STT + Coqui TTS)
- ✅ Gradio web demo
- ✅ CLI interface
- ✅ Automotive QA benchmark (78% accuracy)

### Performance
- 450ms first token latency
- 45 tokens/second generation
- 3.2GB RAM usage

### Installation
See [README.md](https://github.com/sreekar-gajula/tinyllm-auto/blob/main/README.md) for setup instructions.

### Demo
[Link to YouTube demo video]
```

## Step 6: Set Up GitHub Pages (Optional - for Documentation)

1. Go to Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` → `/docs` folder
4. Save

## Step 7: Add Badges to README

Add these badges at the top of your README.md:

```markdown
[![GitHub Stars](https://img.shields.io/github/stars/sreekar-gajula/tinyllm-auto?style=social)](https://github.com/sreekar-gajula/tinyllm-auto/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/sreekar-gajula/tinyllm-auto?style=social)](https://github.com/sreekar-gajula/tinyllm-auto/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/sreekar-gajula/tinyllm-auto)](https://github.com/sreekar-gajula/tinyllm-auto/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/sreekar-gajula/tinyllm-auto/workflows/CI/badge.svg)](https://github.com/sreekar-gajula/tinyllm-auto/actions)
```

## Step 8: Create Additional Files

### Issue Templates

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run '...'
2. Input '...'
3. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**System Information:**
 - OS: [e.g., Ubuntu 22.04]
 - Python Version: [e.g., 3.10]
 - CPU: [e.g., Intel i7-10700K]
 - RAM: [e.g., 8GB]

**Additional context**
Add any other context about the problem here.
```

### Pull Request Template

Create `.github/PULL_REQUEST_TEMPLATE.md`:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] CI checks pass

## Checklist
- [ ] Code follows project style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or clearly documented)
```

## Step 9: Regular Maintenance

### Keep Your Repository Active
- Respond to issues promptly
- Review and merge pull requests
- Update documentation
- Release new versions regularly
- Engage with the community

### Update Your Project
```bash
# Pull latest changes
git pull origin main

# Create a new feature branch
git checkout -b feature/new-feature

# Make changes, commit, and push
git add .
git commit -m "Add new feature"
git push origin feature/new-feature

# Create pull request on GitHub
```

## Step 10: Promote Your Project

1. **Add to lists**:
   - [Awesome LLM](https://github.com/Hannibal046/Awesome-LLM)
   - [Awesome Edge AI](https://github.com/rcmalli/Awesome-Edge-AI)
   - [Awesome Automotive](https://github.com/Marcin214/awesome-automotive)

2. **Share on social media**:
   - Twitter/X with hashtags: #EdgeAI #LLM #Automotive
   - LinkedIn with project description
   - Reddit (r/MachineLearning, r/LocalLLaMA)

3. **Write a blog post** about the project

4. **Create a demo video** and upload to YouTube

## Troubleshooting

### Large Files
If you accidentally committed large model files:
```bash
# Remove from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch models/*.gguf' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (be careful!)
git push origin --force --all
```

### Merge Conflicts
```bash
# Update your branch with main
git checkout main
git pull origin main
git checkout your-branch
git merge main

# Resolve conflicts, then:
git add .
git commit -m "Resolve merge conflicts"
git push
```

## Resources

- [GitHub Documentation](https://docs.github.com)
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Semantic Versioning](https://semver.org/)

---

**Need Help?** Open an issue or reach out to the maintainers!

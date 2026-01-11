# GitHub Setup Guide

This guide will help you push this project to your GitHub repository.

## Prerequisites

- GitHub account (https://github.com/adelrzouga)
- Git configured with your credentials

## Steps to Push to GitHub

### 1. Create a New Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `ircc-xfa-extractor`
3. Description: `Extract filled data from Canadian immigration (IRCC) XFA PDF forms`
4. Make it **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 2. Add GitHub Remote

```bash
cd /Users/adel/Desktop/ircc-xfa-extractor

# Add your GitHub repository as remote
git remote add origin https://github.com/adelrzouga/ircc-xfa-extractor.git

# Verify the remote was added
git remote -v
```

### 3. Push to GitHub

```bash
# Push the main branch to GitHub
git push -u origin main
```

### 4. Verify on GitHub

Visit https://github.com/adelrzouga/ircc-xfa-extractor to see your repository!

## Alternative: Using SSH

If you prefer SSH (recommended for frequent pushes):

```bash
# Add remote with SSH
git remote add origin git@github.com:adelrzouga/ircc-xfa-extractor.git

# Push
git push -u origin main
```

## Repository Settings (Optional)

After pushing, you can configure:

### Add Topics

Go to repository settings → Add topics:
- `pdf`
- `xfa`
- `immigration`
- `canada`
- `ircc`
- `python`
- `cli`
- `data-extraction`

### Add Description

In repository settings:
```
🇨🇦 Extract filled data from Canadian immigration (IRCC) XFA PDF forms
```

### Enable GitHub Pages (Optional)

For documentation hosting:
1. Go to Settings → Pages
2. Source: Deploy from branch `main`
3. Folder: `/docs` or `/ (root)`

## Post-Push Checklist

- [ ] Repository is visible on GitHub
- [ ] README displays properly
- [ ] All files are present
- [ ] License is correct
- [ ] Repository description is set
- [ ] Topics are added

## Making Changes Later

```bash
# Make your changes
git add .
git commit -m "Your commit message"
git push
```

## Collaboration

To allow others to contribute:
1. Go to Settings → Collaborators
2. Add collaborators by username

## Creating Releases

When ready to create a release:

```bash
# Tag the current version
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

Then create a release on GitHub:
1. Go to Releases
2. Click "Create a new release"
3. Select the tag `v1.0.0`
4. Add release notes
5. Publish

## Troubleshooting

### Authentication Issues

If you get authentication errors:

```bash
# Use personal access token
# Go to GitHub → Settings → Developer settings → Personal access tokens
# Generate a new token with 'repo' scope
# Use it as password when pushing
```

### Remote Already Exists

```bash
# If remote already exists, update it
git remote set-url origin https://github.com/adelrzouga/ircc-xfa-extractor.git
```

## Next Steps

1. **Push to GitHub** using the steps above
2. **Test installation** from GitHub:
   ```bash
   pip install git+https://github.com/adelrzouga/ircc-xfa-extractor.git
   ```
3. **Share** with others!
4. **Star** your own repository (it counts! 😄)

---

**Ready to share your work with the world!** 🚀

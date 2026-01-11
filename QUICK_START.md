# Quick Start Guide

Your IRCC XFA Extractor is now live on GitHub! 🎉

**Repository:** https://github.com/adelrzouga/ircc-xfa-extractor

## Installation

### For Others to Install

Anyone can now install your tool directly from GitHub:

```bash
pip install git+https://github.com/adelrzouga/ircc-xfa-extractor.git
```

### For Your Own Computer

To make the `ircc` command available system-wide on your Mac:

#### Option 1: Using pipx (Recommended)
```bash
# Install pipx if you don't have it
brew install pipx

# Install ircc-xfa-extractor
pipx install git+https://github.com/adelrzouga/ircc-xfa-extractor.git

# Now 'ircc' is available globally
ircc --version
```

#### Option 2: Using pip with virtual environment
```bash
python3 -m venv ~/venvs/ircc
~/venvs/ircc/bin/pip install git+https://github.com/adelrzouga/ircc-xfa-extractor.git

# Add alias to your shell profile (~/.zshrc or ~/.bash_profile)
echo 'alias ircc="$HOME/venvs/ircc/bin/ircc"' >> ~/.zshrc
source ~/.zshrc
```

## Usage

```bash
# Extract from a single PDF
ircc /path/to/form.pdf

# Extract from multiple PDFs
ircc ~/Downloads/doc\ Rim\ 2/*.pdf

# With output directory and verbose mode
ircc form.pdf -o ~/extracted --verbose

# Multiple files with combined output
ircc *.pdf --combined -o ~/output
```

## Quick Examples

### Example 1: Extract Your Immigration Forms
```bash
ircc ~/Downloads/imm5257.pdf ~/Downloads/imm5710.pdf \
     -o ~/Documents/immigration_data \
     --combined \
     --verbose
```

### Example 2: Process All PDFs in a Folder
```bash
ircc ~/Downloads/doc\ Rim\ 2/*.pdf -o ~/Desktop/extracted
```

### Example 3: Just the Command You Wanted
```bash
# Simply run:
ircc ~/path/to/form.pdf

# Output will be in the same directory as the PDF
```

## What Was Pushed to GitHub

✅ Complete Python package
✅ CLI tool (`ircc` command)
✅ Comprehensive documentation
✅ MIT License
✅ Examples and usage guides
✅ Contributing guidelines

## Sharing Your Project

Share this with others:
```
🇨🇦 Extract data from Canadian immigration XFA forms with one command!

pip install git+https://github.com/adelrzouga/ircc-xfa-extractor.git

Then use: ircc your-form.pdf
```

## Repository Features Added

- 📌 **Topics**: pdf, xfa, immigration, canada, ircc, python, cli, data-extraction
- 📝 **Description**: "🇨🇦 Extract filled data from Canadian immigration (IRCC) XFA PDF forms"
- 🔓 **Public**: Anyone can view and install
- ⚖️ **License**: MIT (open source)

## Making Updates

When you make changes:

```bash
cd /Users/adel/Desktop/ircc-xfa-extractor

# Make your changes to the code
# Then commit and push
git add .
git commit -m "Your change description"
git push
```

## Creating a Release

When ready for v1.0.0 official release:

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Then create a release on GitHub:
https://github.com/adelrzouga/ircc-xfa-extractor/releases/new

## Support

- **Issues**: https://github.com/adelrzouga/ircc-xfa-extractor/issues
- **Documentation**: Check README.md and USAGE.md in the repository

---

**Congratulations! Your tool is now publicly available!** 🚀

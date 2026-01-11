# Usage Guide

This guide provides detailed examples of how to use the IRCC XFA Form Extractor.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Advanced Examples](#advanced-examples)
- [Integration Examples](#integration-examples)
- [Tips and Tricks](#tips-and-tricks)

## Installation

First, install the tool:

```bash
# Clone and install
git clone https://github.com/adelrzouga/ircc-xfa-extractor.git
cd ircc-xfa-extractor
pip install -e .

# Verify installation
ircc --version
```

## Basic Usage

### Extract Single File

```bash
# Extract data from one form
ircc ~/Downloads/imm5257.pdf
```

Output:
```
✓ imm5257.pdf: 25 fields → imm5257_filled.json
```

### View Extraction Details

```bash
# Use verbose mode to see what's being extracted
ircc ~/Downloads/imm5257.pdf --verbose
```

Output:
```
================================================================================
IRCC XFA Form Extractor v1.0.0
================================================================================

📄 Processing: imm5257.pdf
  ✓ Extracted 25 fields
  ✓ Saved to: /Users/you/Downloads/imm5257_filled.json

  Sample extracted data:
    • Schedule1.FamilyName: CHAFROUD EP BAHRI
    • Schedule1.GivenName: RIM
    • Schedule1.ApplicantBirthDate.Day: 08
    • Schedule1.ApplicantBirthDate.Month: 01
    • Schedule1.ApplicantBirthDate.Year: 1984
    ... and 20 more fields

================================================================================
Summary: 1 succeeded, 0 failed
================================================================================
```

## Advanced Examples

### Process Multiple Files

```bash
# Extract from multiple files
ircc form1.pdf form2.pdf form3.pdf

# Or use wildcards
ircc ~/Documents/immigration/*.pdf
```

### Organize Output

```bash
# Save all extracted JSON files to a specific directory
ircc ~/Downloads/*.pdf -o ~/Documents/extracted_data
```

### Combined Output

```bash
# Create individual files + one combined file
ircc imm5257.pdf imm5710.pdf --combined

# This creates:
# - imm5257_filled.json
# - imm5710_filled.json
# - all_forms_filled.json (combined)
```

The combined file structure:
```json
{
  "imm5257": {
    "Schedule1.FamilyName": "...",
    "Schedule1.GivenName": "..."
  },
  "imm5710": {
    "Page1.PersonalDetails.Name.FamilyName": "...",
    "Page2.ContactInformation.q5-6.Email.Email": "..."
  }
}
```

### Compact JSON Output

```bash
# Generate compact JSON (no indentation)
ircc form.pdf -f json

# Useful for programmatic processing or smaller file sizes
```

## Integration Examples

### Python Script Integration

```python
#!/usr/bin/env python3
from ircc_xfa import extract_xfa_filled_data
import json

# Extract data
data = extract_xfa_filled_data('/path/to/form.pdf')

# Process the data
print(f"Found {len(data)} fields")

# Access specific fields
family_name = data.get('Schedule1.FamilyName', 'N/A')
email = data.get('Page2.ContactInformation.q5-6.Email.Email', 'N/A')

print(f"Name: {family_name}")
print(f"Email: {email}")

# Save to custom format
with open('custom_output.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Batch Processing Script

```bash
#!/bin/bash
# batch_extract.sh - Process all PDFs in a directory

INPUT_DIR="$HOME/Documents/immigration_forms"
OUTPUT_DIR="$HOME/Documents/extracted"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Process all PDFs
for pdf in "$INPUT_DIR"/*.pdf; do
    echo "Processing: $(basename "$pdf")"
    ircc "$pdf" -o "$OUTPUT_DIR"
done

# Create combined output
ircc "$INPUT_DIR"/*.pdf -o "$OUTPUT_DIR" --combined

echo "Done! Results in $OUTPUT_DIR"
```

### Data Analysis Example

```python
#!/usr/bin/env python3
"""
Analyze extracted immigration form data
"""
import json
from pathlib import Path
from collections import Counter

def analyze_forms(directory):
    """Analyze all extracted JSON files in a directory"""

    json_files = Path(directory).glob('*_filled.json')

    all_data = []
    field_counts = Counter()

    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)
            all_data.append(data)
            field_counts.update(data.keys())

    print(f"Analyzed {len(all_data)} forms")
    print(f"\nMost common fields:")
    for field, count in field_counts.most_common(10):
        print(f"  {field}: {count} forms")

    return all_data

# Usage
if __name__ == '__main__':
    data = analyze_forms('./extracted')
```

## Tips and Tricks

### 1. Quick Check of PDF Content

```bash
# Use verbose mode to preview data without opening JSON
ircc form.pdf -v | head -20
```

### 2. Filter Specific Forms

```bash
# Only process IMM5710 forms
ircc ~/Downloads/imm5710*.pdf -o ./work_permits
```

### 3. Create Aliases for Common Tasks

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# Quick extraction alias
alias ircc-extract='ircc --verbose --combined'

# Usage
ircc-extract ~/Downloads/*.pdf -o ~/extracted
```

### 4. Verify Before Extraction

```bash
# Check if file is XFA-based
file your_form.pdf
# Should show: PDF document, version X.X

# Try extraction with verbose mode
ircc your_form.pdf -v
```

### 5. Handle Errors Gracefully

```bash
# Process all PDFs, even if some fail
for pdf in *.pdf; do
    ircc "$pdf" 2>> errors.log || echo "Failed: $pdf"
done
```

### 6. Automated Workflow

```bash
#!/bin/bash
# auto_extract.sh - Monitor folder and auto-extract

WATCH_DIR="$HOME/Downloads"
OUTPUT_DIR="$HOME/Documents/extracted_forms"

# Use fswatch or inotify-tools
fswatch -0 "$WATCH_DIR" | while read -d "" event; do
    if [[ "$event" == *.pdf ]]; then
        echo "New PDF detected: $event"
        ircc "$event" -o "$OUTPUT_DIR" --verbose
    fi
done
```

## Common Scenarios

### Scenario 1: Immigration Consultant

```bash
# Process all client forms and organize by type
mkdir -p extracted/{applications,work_permits,visitor_visas}

ircc client_forms/imm5257*.pdf -o extracted/applications
ircc client_forms/imm5710*.pdf -o extracted/work_permits
ircc client_forms/imm5257e*.pdf -o extracted/visitor_visas

# Create summary report
ls -lh extracted/*/*.json | wc -l
echo "Total forms processed"
```

### Scenario 2: Personal Application Tracking

```bash
# Extract your own application data
ircc ~/Documents/my_application/*.pdf \
    -o ~/Documents/my_application/extracted \
    --combined \
    --verbose

# Review the combined output
cat ~/Documents/my_application/extracted/all_forms_filled.json | jq .
```

### Scenario 3: Data Migration

```bash
# Extract data from old PDFs to import into new system
ircc archive/*.pdf -o migration_data -f json --combined

# The compact JSON can be imported into databases or other systems
```

## Troubleshooting

### Issue: "No filled data found"

**Solution**: The form may be empty. Open the PDF and verify fields are filled.

```bash
# Check PDF structure
pdfinfo your_form.pdf

# Try verbose mode to see details
ircc your_form.pdf --verbose
```

### Issue: Permission denied

**Solution**: Check file permissions

```bash
# Make PDF readable
chmod 644 your_form.pdf

# Make output directory writable
mkdir -p output && chmod 755 output
```

### Issue: Command not found

**Solution**: Ensure installation completed

```bash
# Reinstall
pip install -e . --force-reinstall

# Check PATH
which ircc

# If not found, use full path
python -m ircc_xfa.cli your_form.pdf
```

## Additional Resources

- See [README.md](README.md) for general information
- Check [examples/](examples/) for sample outputs
- Report issues on [GitHub](https://github.com/adelrzouga/ircc-xfa-extractor/issues)

---

**Happy extracting!** 🎉

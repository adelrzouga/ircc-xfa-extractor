# IRCC XFA Form Extractor

A Python command-line tool to extract filled data from Canadian immigration (IRCC) XFA PDF forms.

## Features

- 🔍 **Smart Extraction**: Extracts only filled data, ignoring form templates and options
- 📄 **Multiple Formats**: Supports all IRCC XFA forms (IMM5257, IMM5710, etc.)
- 💾 **JSON Output**: Saves extracted data in structured JSON format
- 🚀 **Easy to Use**: Simple command-line interface
- 🔧 **Flexible**: Process single or multiple files at once

## Installation

### Method 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/adelrzouga/ircc-xfa-extractor.git
cd ircc-xfa-extractor

# Install the package
pip install -e .
```

### Method 2: Direct Installation

```bash
pip install git+https://github.com/adelrzouga/ircc-xfa-extractor.git
```

### Requirements

- Python 3.8 or higher
- pikepdf (automatically installed with the package)

## Usage

### Basic Usage

Extract data from a single PDF:

```bash
ircc /path/to/form.pdf
```

This will create a JSON file named `form_filled.json` in the same directory as the PDF.

### Advanced Usage

```bash
# Process multiple files
ircc /path/to/imm5257.pdf /path/to/imm5710.pdf

# Specify output directory
ircc /path/to/form.pdf -o /output/directory

# Create combined output file
ircc /path/to/*.pdf --combined

# Compact JSON format
ircc /path/to/form.pdf -f json

# Verbose output with details
ircc /path/to/form.pdf --verbose
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `files` | One or more PDF files to process (required) |
| `-o, --output DIR` | Output directory for JSON files (default: same as PDF) |
| `-f, --format {json,pretty}` | Output format: compact or indented (default: pretty) |
| `-c, --combined` | Create a combined JSON file with all extracted data |
| `-v, --verbose` | Show detailed extraction information |
| `--version` | Show version information |

## Examples

### Example 1: Process Immigration Application

```bash
# Extract data from application form
ircc ~/Downloads/imm5257.pdf

# Output: ~/Downloads/imm5257_filled.json
```

### Example 2: Process Multiple Forms

```bash
# Extract from all PDF forms in a directory
ircc ~/Documents/immigration/*.pdf -o ~/Documents/extracted --combined

# Creates individual JSON files for each PDF plus a combined file
```

### Example 3: Detailed Extraction

```bash
# Get detailed output about what's being extracted
ircc application.pdf --verbose
```

Output:
```
================================================================================
IRCC XFA Form Extractor v1.0.0
================================================================================

📄 Processing: imm5257.pdf
  ✓ Extracted 25 fields
  ✓ Saved to: imm5257_filled.json

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

## Supported Forms

This tool works with any IRCC XFA-based PDF form, including but not limited to:

- **IMM 5257** - Application for Temporary Resident Visa
- **IMM 5710** - Application to Change Conditions, Extend Stay or Remain in Canada
- **IMM 5406** - Additional Family Information
- **IMM 5476** - Use of a Representative
- And many more...

## Output Format

The tool extracts data into clean, structured JSON:

```json
{
  "Schedule1.FamilyName": "CHAFROUD EP BAHRI",
  "Schedule1.GivenName": "RIM",
  "Schedule1.ApplicantBirthDate.Day": "08",
  "Schedule1.ApplicantBirthDate.Month": "01",
  "Schedule1.ApplicantBirthDate.Year": "1984",
  "Schedule1.UCI": "1129825035",
  "Page1.PersonalDetails.Name.FamilyName": "CHAFROUD EP BAHRI",
  "Page2.ContactInformation.q5-6.Email.Email": "rim.chafroud@gmail.com",
  "Page2.Passport.PassportNum": "J454097"
}
```

## How It Works

1. **Opens PDF**: Uses pikepdf to read the PDF structure
2. **Locates XFA Data**: Finds the XFA datasets section containing form data
3. **Parses XML**: Extracts the XML structure from XFA streams
4. **Filters Data**: Intelligently distinguishes between:
   - Actual filled values (names, dates, addresses)
   - Form template options (dropdown choices, checkboxes)
5. **Saves JSON**: Outputs clean, structured data

## Troubleshooting

### "PDF does not contain XFA data"

Some PDF forms may not use XFA format. This tool specifically works with XFA-based forms. Most IRCC forms from the official website are XFA-based.

### "No filled data found"

This means the PDF doesn't have any filled fields, or the form hasn't been completed yet. Try opening the PDF and verifying that fields are actually filled in.

### Permission Errors

Make sure you have read access to the PDF file and write access to the output directory.

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/adelrzouga/ircc-xfa-extractor.git
cd ircc-xfa-extractor

# Install in development mode with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black ircc_xfa/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with [pikepdf](https://github.com/pikepdf/pikepdf) for PDF processing
- Designed for Canadian immigration (IRCC) XFA forms

## Disclaimer

This tool is for personal use and data extraction purposes. Always verify extracted data against the original PDF forms. This is not an official IRCC tool and is not affiliated with Immigration, Refugees and Citizenship Canada.

## Author

**Adel Rzouga**
- GitHub: [@adelrzouga](https://github.com/adelrzouga)

## Support

If you encounter any issues or have questions:
- Open an issue on [GitHub](https://github.com/adelrzouga/ircc-xfa-extractor/issues)
- Check existing issues for solutions

---

**Made with ❤️ for the Canadian immigration community**

#!/usr/bin/env python3
"""
Command-line interface for IRCC XFA Form Extractor
"""
import argparse
import json
import sys
from pathlib import Path
from typing import List

from . import __version__, __description__
from .extractor import extract_xfa_filled_data


def setup_parser():
    """Set up command-line argument parser"""
    parser = argparse.ArgumentParser(
        prog='ircc',
        description=__description__,
        epilog='Extract filled data from Canadian immigration XFA PDF forms'
    )

    parser.add_argument(
        'files',
        nargs='+',
        help='Path to one or more PDF files to extract data from'
    )

    parser.add_argument(
        '-o', '--output',
        help='Output directory for JSON files (default: same as PDF location)',
        type=Path
    )

    parser.add_argument(
        '-f', '--format',
        choices=['json', 'pretty'],
        default='pretty',
        help='Output format: json (compact) or pretty (indented, default)'
    )

    parser.add_argument(
        '-c', '--combined',
        action='store_true',
        help='Create a combined output file with all extracted data'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output showing extraction details'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )

    return parser


def process_pdf(pdf_path: Path, output_dir: Path, format_type: str, verbose: bool) -> dict:
    """
    Process a single PDF file and save extracted data

    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save output JSON
        format_type: 'json' or 'pretty'
        verbose: Whether to print verbose output

    Returns:
        dict: Extracted data
    """
    if verbose:
        print(f"\n📄 Processing: {pdf_path.name}")

    try:
        # Extract data
        data = extract_xfa_filled_data(str(pdf_path))

        if not data:
            print(f"  ⚠️  Warning: No filled data found in {pdf_path.name}")
            return {}

        # Determine output path
        output_file = output_dir / f"{pdf_path.stem}_filled.json"

        # Save to JSON
        indent = 2 if format_type == 'pretty' else None
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)

        if verbose:
            print(f"  ✓ Extracted {len(data)} fields")
            print(f"  ✓ Saved to: {output_file}")

            # Show some sample data
            print(f"\n  Sample extracted data:")
            for i, (key, value) in enumerate(list(data.items())[:5]):
                display_value = str(value)[:60] + "..." if len(str(value)) > 60 else str(value)
                print(f"    • {key}: {display_value}")
            if len(data) > 5:
                print(f"    ... and {len(data) - 5} more fields")
        else:
            print(f"✓ {pdf_path.name}: {len(data)} fields → {output_file.name}")

        return data

    except FileNotFoundError:
        print(f"  ✗ Error: File not found: {pdf_path}", file=sys.stderr)
        return {}
    except ValueError as e:
        print(f"  ✗ Error: {e}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}", file=sys.stderr)
        if verbose:
            import traceback
            traceback.print_exc()
        return {}


def main():
    """Main CLI entry point"""
    parser = setup_parser()
    args = parser.parse_args()

    # Display header
    if args.verbose:
        print("=" * 80)
        print(f"IRCC XFA Form Extractor v{__version__}")
        print("=" * 80)

    # Process all files
    all_data = {}
    success_count = 0
    error_count = 0

    for file_path in args.files:
        pdf_path = Path(file_path).expanduser().resolve()

        if not pdf_path.exists():
            print(f"✗ File not found: {pdf_path}", file=sys.stderr)
            error_count += 1
            continue

        if not pdf_path.suffix.lower() == '.pdf':
            print(f"✗ Not a PDF file: {pdf_path}", file=sys.stderr)
            error_count += 1
            continue

        # Determine output directory
        output_dir = args.output if args.output else pdf_path.parent
        output_dir = Path(output_dir).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        # Process the PDF
        data = process_pdf(pdf_path, output_dir, args.format, args.verbose)

        if data:
            all_data[pdf_path.stem] = data
            success_count += 1
        else:
            error_count += 1

    # Create combined output if requested
    if args.combined and all_data:
        combined_path = (args.output if args.output else Path.cwd()) / "all_forms_filled.json"
        indent = 2 if args.format == 'pretty' else None

        with open(combined_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, indent=indent, ensure_ascii=False)

        if args.verbose:
            print(f"\n📦 Combined output saved to: {combined_path}")
        else:
            print(f"✓ Combined: {combined_path.name}")

    # Summary
    if args.verbose or (success_count + error_count) > 1:
        print("\n" + "=" * 80)
        print(f"Summary: {success_count} succeeded, {error_count} failed")
        print("=" * 80)

    # Exit with appropriate code
    sys.exit(0 if error_count == 0 else 1)


if __name__ == '__main__':
    main()

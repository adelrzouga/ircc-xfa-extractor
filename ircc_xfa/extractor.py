#!/usr/bin/env python3
"""
Core extraction logic for XFA forms
"""
import xml.etree.ElementTree as ET
import pikepdf


def extract_filled_values(root):
    """
    Extract only filled values from XFA datasets

    XFA forms typically have structure like:
    <xfa:datasets><xfa:data><form1>
        <field1>value</field1>
        <field2>value</field2>
    </form1></xfa:data></xfa:datasets>

    Args:
        root: ElementTree root of XFA datasets XML

    Returns:
        dict: Dictionary of field names and their filled values
    """
    filled_data = {}

    # Navigate to the actual data section
    ns = {'xfa': 'http://www.xfa.org/schema/xfa-data/1.0/'}

    # Try to find the data section
    data_section = root.find('.//xfa:data', ns)
    if data_section is None:
        data_section = root.find('.//data')

    if data_section is None:
        data_section = root

    # Find the form root (usually form1 or IMM****E_1)
    form_root = None
    for child in data_section:
        tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
        if tag.startswith('form') or tag.startswith('IMM'):
            form_root = child
            break

    if form_root is None:
        form_root = data_section

    def extract_fields(element, prefix=""):
        """Recursively extract field values from XFA XML"""
        for child in element:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag

            # Skip known structural/template elements
            if tag in ['xfa:datasets', 'xfa:data', 'datasets', 'data']:
                extract_fields(child, prefix)
                continue

            # Build field name
            field_name = f"{prefix}.{tag}" if prefix else tag

            # Check if this element has a text value
            if child.text and child.text.strip():
                value = child.text.strip()

                # Skip if it looks like a form option/template value
                # Real data usually has: dates, numbers, addresses, names
                common_options = {
                    'yes', 'no', 'male', 'female', 'english', 'french',
                    'married', 'single', 'other', 'both', 'neither'
                }

                # Only add if it's likely real data:
                # - Contains numbers (dates, phone, postal codes)
                # - Contains @ (email)
                # - Multiple words (names, addresses)
                # - Long text (descriptions)
                # - Not a common single option
                value_lower = value.lower()
                is_real_data = (
                    any(c.isdigit() for c in value) or
                    '@' in value or
                    ' ' in value or
                    len(value) > 20 or
                    (len(value) > 2 and value_lower not in common_options)
                )

                if is_real_data:
                    # Clean up field name - remove form root prefix
                    field_name = (field_name
                                  .replace('form1.', '')
                                  .replace('IMM5257E_1.', '')
                                  .replace('IMM5710E_1.', ''))
                    filled_data[field_name] = value

            # Recurse into children
            if len(child) > 0:
                extract_fields(child, field_name)

    extract_fields(form_root)
    return filled_data


def extract_xfa_filled_data(pdf_path):
    """
    Extract filled XFA form values from a PDF file

    Args:
        pdf_path: Path to the PDF file containing XFA forms

    Returns:
        dict: Dictionary of field names and their filled values

    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If PDF doesn't contain XFA forms
    """
    form_data = {}

    try:
        with pikepdf.open(pdf_path) as pdf:
            # Check for XFA forms
            if '/AcroForm' not in pdf.Root:
                raise ValueError(f"PDF {pdf_path} does not contain AcroForm")

            if '/XFA' not in pdf.Root.AcroForm:
                raise ValueError(f"PDF {pdf_path} does not contain XFA data")

            xfa = pdf.Root.AcroForm.XFA

            # Convert to list (handles pikepdf Array type)
            try:
                xfa_list = list(xfa)
            except TypeError:
                raise ValueError("XFA data in unexpected format")

            # Process XFA array (stored as name/stream pairs)
            for i in range(0, len(xfa_list), 2):
                if i + 1 < len(xfa_list):
                    name = str(xfa_list[i])
                    stream = xfa_list[i + 1]

                    # Extract data from datasets section
                    if 'datasets' in name.lower() and hasattr(stream, 'read_bytes'):
                        try:
                            data = stream.read_bytes()
                            xml_str = data.decode('utf-8')
                            root = ET.fromstring(xml_str)
                            form_data = extract_filled_values(root)
                        except ET.ParseError as e:
                            raise ValueError(f"Failed to parse XFA XML: {e}")
                        except UnicodeDecodeError as e:
                            raise ValueError(f"Failed to decode XFA data: {e}")

    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    except Exception as e:
        if isinstance(e, (ValueError, FileNotFoundError)):
            raise
        raise RuntimeError(f"Error processing {pdf_path}: {e}")

    return form_data

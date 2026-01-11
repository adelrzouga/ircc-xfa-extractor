"""
IRCC XFA Form Extractor
Extract filled data from Canadian immigration XFA PDF forms
"""

__version__ = "1.0.0"
__author__ = "Adel Rzouga"
__description__ = "Extract filled data from IRCC XFA PDF forms"

from .extractor import extract_xfa_filled_data, extract_filled_values

__all__ = ["extract_xfa_filled_data", "extract_filled_values"]

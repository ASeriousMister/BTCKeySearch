#!/usr/bin/env python3

import os
import argparse
import re
import sys
from pathlib import Path

#pip install python-docx pypdf2

# Try importing third-party libraries safely
try:
    import docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    from PyPDF2 import PdfReader
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# Regex Patterns
PATTERNS = {
    'BTC Private Key (WIF)': re.compile(r'\b[5KL][1-9A-HJ-NP-Za-km-z]{50,51}\b'),
    'BIP32 Root Key (xprv)': re.compile(r'\bxprv[a-km-zA-HJ-NP-Z1-9]{107,108}\b'),
    #'Monero Spend Key': re.compile(r'\b[0-9a-fA-F]{62}[0][0-9a-fA-F]\b'),
    # Added Ethereum Private Key (64 hex chars, strict check to avoid hash false positives)
    #'ETH Private Key': re.compile(r'\b0x[a-fA-F0-9]{64}\b') 
}

# Binary extensions to skip to save time
IGNORE_EXTS = {'.jpg', '.jpeg', '.png', '.gif', '.zip', '.tar', '.gz', '.exe', '.dll', '.so', '.pyc'}

def get_docx_text(filepath):
    """Extracts text from DOCX in memory."""
    if not HAS_DOCX:
        return ""
    try:
        doc = docx.Document(filepath)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception:
        return ""

def get_pdf_text(filepath):
    """Extracts text from PDF in memory."""
    if not HAS_PDF:
        return ""
    try:
        reader = PdfReader(filepath)
        text = []
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text.append(content)
        return '\n'.join(text)
    except Exception:
        return ""

def scan_content(content, filename, file_path):
    """Scans a string of text for regex matches."""
    found_any = False
    
    # Iterate over lines to give line numbers (simulated for PDFs/DOCs)
    lines = content.splitlines()
    
    for line_idx, line in enumerate(lines, 1):
        for label, pattern in PATTERNS.items():
            matches = pattern.findall(line)
            for match in matches:
                if not found_any:
                    print(f"{Color.DARKCYAN}\n======== Matches in {filename} ========{Color.END}")
                    print(f"Path: {file_path}")
                    found_any = True
                
                print(f"{Color.GREEN}[{label}]{Color.END} Line {line_idx}: {match}")

def process_file(filepath):
    """Determines how to read the file and triggers the scan."""
    path_obj = Path(filepath)
    
    # Skip ignored extensions
    if path_obj.suffix.lower() in IGNORE_EXTS:
        return

    content = ""

    try:
        # Handle specific formats
        if path_obj.suffix.lower() == '.docx':
            content = get_docx_text(filepath)
        elif path_obj.suffix.lower() == '.pdf':
            content = get_pdf_text(filepath)
        else:
            # Handle standard text files
            # 'errors=replace' ensures binary junk doesn't crash the script
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

        if content:
            scan_content(content, path_obj.name, filepath)

    except (PermissionError, OSError):
        # Silently skip files we can't read (system files, etc)
        pass
    except Exception as e:
        print(f"{Color.RED}Error reading {filepath}: {e}{Color.END}")

def main():
    print(Color.YELLOW + '\n*=*=*= Bitcoin Key Search =*=*=*\n' + Color.END)
    
    parser = argparse.ArgumentParser(description='Cryptocurrency private key finder')
    parser.add_argument('-d', metavar='directory', type=str, required=True, help='Directory to scan')
    args = parser.parse_args()
    
    target_dir = Path(args.d)

    if not target_dir.exists():
        sys.exit(f"{Color.RED}Directory does not exist!{Color.END}")

    print(f"Scanning directory: {target_dir.resolve()}")
    print("Press Ctrl+C to stop...\n")

    try:
        # os.walk is more efficient than manual recursion
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                filepath = os.path.join(root, file)
                process_file(filepath)
                
    except KeyboardInterrupt:
        print(f"\n{Color.RED}Scan interrupted by user.{Color.END}")

    print(f"\n{Color.YELLOW}Scan complete.{Color.END}")

if __name__ == "__main__":
    main()

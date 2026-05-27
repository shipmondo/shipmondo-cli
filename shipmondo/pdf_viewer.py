import base64
import tempfile
import os
import subprocess
import platform
import sys

def open_file_cross_platform(filepath: str):
    """Platform-agnostic file opener."""
    try:
        current_os = platform.system()
        if current_os == 'Darwin':
            subprocess.call(('open', filepath))
        elif current_os == 'Windows':
            os.startfile(filepath)
        else:
            subprocess.call(('xdg-open', filepath))
    except Exception as e:
        print(f'{{"error": "Could not launch PDF viewer", "details": "{e}"}}', file=sys.stderr)

def extract_and_open_pdfs(data: dict, prefix="shipmondo_label_"):
    """Recursively search for base64 PDF strings, decode them, and open them."""
    found_count = 0
    
    def search_and_decode(node):
        nonlocal found_count
        if isinstance(node, dict):
            for k, v in node.items():
                if isinstance(v, str) and v.startswith("JVBERi0"):
                    save_and_open(v)
                    found_count += 1
                else:
                    search_and_decode(v)
        elif isinstance(node, list):
            for item in node:
                search_and_decode(item)
                
    def save_and_open(b64_string):
        try:
            pdf_bytes = base64.b64decode(b64_string)
            fd, path = tempfile.mkstemp(prefix=prefix, suffix=".pdf")
            with os.fdopen(fd, 'wb') as f:
                f.write(pdf_bytes)
            
            print(f"📄 [PDF Extracted] Opening: {path}", file=sys.stderr)
            open_file_cross_platform(path)
        except Exception as e:
            print(f'{{"error": "Failed to decode PDF string", "details": "{e}"}}', file=sys.stderr)

    search_and_decode(data)
    
    if found_count == 0:
        print("⚠️ No base64 PDFs were found in this API response.", file=sys.stderr)

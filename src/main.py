import sys
from pathlib import Path
from utils import copy_static_to_public
from generate import generate_pages_recursive
import shutil

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    docs_dir = Path("docs")
    static_dir = Path("static")
    content_dir = Path("content")
    template_file = Path("template.html")

    # Delete existing docs directory
    if docs_dir.exists():
        shutil.rmtree(docs_dir)

    # Copy static files
    copy_static_to_public(str(static_dir), str(docs_dir))

    # Generate all pages recursively with basepath
    generate_pages_recursive(
        content_dir=str(content_dir),
        template_path=str(template_file),
        dest_dir=str(docs_dir),
        basepath=basepath
    )

    print(f"Site generation complete! Basepath: {basepath}")

if __name__ == "__main__":
    main()

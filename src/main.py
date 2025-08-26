from pathlib import Path
from utils import copy_static_to_public
from generate import generate_pages_recursive
import shutil

def main():
    public_dir = Path("public")
    static_dir = Path("static")
    content_dir = Path("content")
    template_file = Path("template.html")

    # 1️⃣ Delete everything in public/
    if public_dir.exists():
        print(f"Clearing public directory: {public_dir}")
        shutil.rmtree(public_dir)

    # 2️⃣ Copy static files from static/ to public/
    print(f"Copying static files from {static_dir} to {public_dir}")
    copy_static_to_public(str(static_dir), str(public_dir))

    # 3️⃣ Generate page from content/index.md
    generate_pages_recursive(
        content_dir=str(content_dir),
        template_path=str(template_file),
        dest_dir=str(public_dir)
    )

    print("Site generation complete!")

if __name__ == "__main__":
    main()

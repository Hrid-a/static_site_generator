import os
from pathlib import Path
from mardwontohtml import markdown_to_html_node
from utils import extract_title

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown content
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Read template content
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    # Extract page title
    title = extract_title(markdown_content)

    # Replace placeholders in template
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    dest_dir = Path(dest_path).parent
    os.makedirs(dest_dir, exist_ok=True)

    # Write final HTML to destination file
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Page generated at: {dest_path}")



def generate_pages_recursive(content_dir: str, template_path: str, dest_dir: str):
    """
    Recursively generate HTML pages for all markdown files in `content_dir`.
    Writes the generated HTML to `dest_dir`, preserving directory structure.
    """
    content_dir = Path(content_dir)
    dest_dir = Path(dest_dir)

    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                md_path = Path(root) / file

                # Preserve directory structure in destination
                relative_path = md_path.relative_to(content_dir).with_suffix(".html")
                dest_path = dest_dir / relative_path

                # Ensure destination directories exist
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Generate the page
                generate_page(
                    from_path=str(md_path),
                    template_path=str(template_path),
                    dest_path=str(dest_path)
                )

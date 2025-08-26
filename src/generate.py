import os
from pathlib import Path
from mardwontohtml import markdown_to_html_node
from utils import extract_title

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    title = extract_title(markdown_content)

    # Replace placeholders
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Replace root-relative paths with basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Ensure destination directories exist
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"Page generated at: {dest_path}")


def generate_pages_recursive(content_dir: str, template_path: str, dest_dir: str, basepath: str = "/"):
    content_dir = Path(content_dir)
    dest_dir = Path(dest_dir)

    for root, dirs, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                md_path = Path(root) / file
                relative_path = md_path.relative_to(content_dir).with_suffix(".html")
                dest_path = dest_dir / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                generate_page(
                    from_path=str(md_path),
                    template_path=str(template_path),
                    dest_path=str(dest_path),
                    basepath=basepath
                )

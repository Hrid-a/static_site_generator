import re
import os
import shutil
from leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINK:
        if not text_node.url:
            raise ValueError("LINK TextNode requires a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})

    elif text_node.text_type == TextType.IMAGE:
        if not text_node.url:
            raise ValueError("IMAGE TextNode requires a URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    else:
        raise ValueError(f"Unsupported TextType: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        else:
            parts = node.text.split(delimiter)
            split_nodes = []

            if len(parts) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            for i in range(len(parts)):
                if parts[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(parts[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(parts[i], text_type))
            new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if not images:
            new_nodes.append(node)
            continue

        for alt, url in images:
            # split once per match
            before, after = text.split(f"![{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after

        if text:  # leftover text after last image
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if not links:
            new_nodes.append(node)
            continue

        for alt, url in links:
            before, after = text.split(f"[{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            text = after

        if text:  # leftover text after last link
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text: str):
    # Start with a single node containing the whole text
    nodes = [TextNode(text, TextType.TEXT)]

    # Apply all your splitters one after another
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        lines = block.split("\n")
        # strip each line individually
        cleaned_lines = [line.strip() for line in lines if line.strip() != ""]
        cleaned_blocks.append("\n".join(cleaned_lines))
    return cleaned_blocks

def copy_static_to_public(src: str, dest: str):
    """
    Recursively copies all files and folders from `src` to `dest`.
    First clears out all existing contents of `dest`.
    """
    # Step 1: Remove destination folder if it exists
    if os.path.exists(dest):
        print(f"Clearing destination directory: {dest}")
        shutil.rmtree(dest)

    # Step 2: Recreate destination folder
    os.makedirs(dest, exist_ok=True)

    # Step 3: Recursive copy function
    def recursive_copy(src_path, dest_path):
        for item in os.listdir(src_path):
            src_item = os.path.join(src_path, item)
            dest_item = os.path.join(dest_path, item)

            if os.path.isdir(src_item):
                # Create the subdirectory in destination
                os.makedirs(dest_item, exist_ok=True)
                print(f"Entering directory: {src_item}")
                recursive_copy(src_item, dest_item)
            else:
                # Copy file
                shutil.copy2(src_item, dest_item)
                print(f"Copied file: {src_item} -> {dest_item}")

    recursive_copy(src, dest)

def extract_title(markdown: str) -> str:
    """
    Extracts the first H1 header from a markdown string.
    Raises ValueError if no H1 header is found.
    """
    lines = markdown.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith("# ") and not line.startswith("##"):  # only single #
            return line[2:].strip()  # remove '# ' and strip spaces
    raise ValueError("No H1 header found in markdown")

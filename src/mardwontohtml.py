from parentnode import ParentNode
from leafnode import LeafNode
from utils import markdown_to_blocks, text_to_textnodes, text_node_to_html_node
from blocktype import BlockType, block_to_block_type


def text_to_children(text: str):
    """
    Converts inline markdown text to a list of HTML nodes,
    ignoring any empty text nodes.
    """
    nodes = text_to_textnodes(text)
    children = [
        text_node_to_html_node(node)
        for node in nodes
        if node.text.strip() != ""  # ignore empty text nodes
    ]
    return children


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown.strip())  # <- strip here
    children = []

    for block in blocks:
        if not block.strip():
            continue  # skip empty blocks

        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            paragraph_text = " ".join(block.split("\n"))
            children.append(ParentNode("p", text_to_children(paragraph_text)))

        elif block_type == BlockType.HEADING:
            first_line = block.split("\n")[0]
            level = len(first_line.split(" ")[0])
            text = first_line[level + 1 :]
            children.append(ParentNode(f"h{level}", text_to_children(text)))

        elif block_type == BlockType.CODE:
            code_text = block.strip("`").strip()
            code_node = LeafNode("code", code_text)
            children.append(ParentNode("pre", [code_node]))

        elif block_type == BlockType.QUOTE:
            lines = [line.lstrip("> ").rstrip() for line in block.split("\n")]
            text = " ".join(lines)
            children.append(ParentNode("blockquote", text_to_children(text)))

        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                item_text = line[2:].strip()
                items.append(ParentNode("li", text_to_children(item_text)))
            children.append(ParentNode("ul", items))

        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                item_text = line.split(". ", 1)[1].strip()
                items.append(ParentNode("li", text_to_children(item_text)))
            children.append(ParentNode("ol", items))

    return ParentNode("div", children)

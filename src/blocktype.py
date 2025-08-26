from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    # Heading: starts with 1–6 '#' followed by a space
    if block.startswith("#"):
        first_word = lines[0].split(" ", 1)
        if len(first_word) > 1:
            hashes = first_word[0]
            if 1 <= len(hashes) <= 6 and all(c == "#" for c in hashes):
                return BlockType.HEADING

    # Code block: starts and ends with triple backticks
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote block: every line starts with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: every line starts with "n. "
    if all(line.lstrip().split(" ", 1)[0][:-1].isdigit() and 
           line.lstrip().split(" ", 1)[0].endswith(".") 
           for line in lines):
        # Validate correct incrementing order
        expected = 1
        for line in lines:
            prefix = line.split(" ", 1)[0]  # e.g. "1."
            number = int(prefix[:-1])
            if number != expected:
                break
            expected += 1
        else:
            return BlockType.ORDERED_LIST

    # Default: paragraph
    return BlockType.PARAGRAPH

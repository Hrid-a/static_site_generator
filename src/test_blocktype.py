import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading text"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Small heading"), BlockType.HEADING)

    def test_code_block(self):
        code = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code), BlockType.CODE)

    def test_quote_block(self):
        quote = "> first line\n> second line"
        self.assertEqual(block_to_block_type(quote), BlockType.QUOTE)

    def test_unordered_list(self):
        ul = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(ul), BlockType.UNORDERED_LIST)

    def test_ordered_list_valid(self):
        ol = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(ol), BlockType.ORDERED_LIST)

    def test_ordered_list_invalid_numbering(self):
        bad_ol = "1. first\n3. wrong"
        self.assertEqual(block_to_block_type(bad_ol), BlockType.PARAGRAPH)

    def test_paragraph(self):
        text = "Just a normal paragraph of text."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

import unittest
from textnode import TextNode, TextType
from utils import (text_node_to_html_node, 
                   split_nodes_delimiter, 
                   extract_markdown_images, 
                   extract_markdown_links, 
                   split_nodes_image, 
                   split_nodes_link, 
                   text_to_textnodes, 
                   markdown_to_blocks,
                   extract_title)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type_text(self):
        node = TextNode("plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "plain text")

    def test_text_type_bold(self):
        node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")

    def test_text_type_italic(self):
        node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")

    def test_text_type_code(self):
        node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")

    def test_text_type_link(self):
        node = TextNode("Google", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_text_type_link_missing_url_raises(self):
        node = TextNode("Google", TextType.LINK, None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text_type_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "image.png", "alt": "Alt text"})

    def test_text_type_image_missing_url_raises(self):
        node = TextNode("Alt text", TextType.IMAGE, None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_invalid_text_type_raises(self):
        class FakeType:
            pass

        node = TextNode("oops", FakeType())
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


class TestSplitNodesDelimter(unittest.TestCase):
    def test_split_nodes_delimiter_valid(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[2].text, " word")

    def test_split_nodes_delimiter_invalid(self):
        node = TextNode("This is text without `proper delimiters", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], images)

    def test_extract_markdown_links(self):
        text = "This is text with a [Google](https://google.com) link and [GitHub](https://github.com) link"
        links = extract_markdown_links(text)
        self.assertListEqual([("Google", "https://google.com"), ("GitHub", "https://github.com")], links)

    def test_split_nodes_image_multiple(self):
        node = TextNode(
            "Start ![first](http://img1.png) middle ![second](http://img2.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "http://img1.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "http://img2.png"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        # Should return the same node untouched
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_multiple(self):
        node = TextNode(
            "Links: [Google](https://google.com) and [Boot](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("Boot", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_split_nodes_link_no_links(self):
        node = TextNode("Nothing to link here", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        # Should return the same node untouched
        self.assertListEqual([node], new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_complex(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_plain(self):
        text = "Just plain text, nothing fancy."
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [TextNode("Just plain text, nothing fancy.", TextType.TEXT)],
            nodes,
        )


class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
                This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
            """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )




class TestExtractTitle(unittest.TestCase):
    def test_simple_h1(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")

    def test_h1_with_whitespace(self):
        md = "   #   My Title   "
        self.assertEqual(extract_title(md), "My Title")

    def test_ignore_h2_or_more(self):
        md = """
        ## Subtitle
        # Main Title
        """
        self.assertEqual(extract_title(md), "Main Title")

    def test_no_h1_raises(self):
        md = """
        ## Subtitle
        Some paragraph text
        """
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()

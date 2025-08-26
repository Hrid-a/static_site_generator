import unittest

from htmlnode import HtmlNode


class TestHtmlNode(unittest.TestCase):
    def test_init(self):
        node = HtmlNode(tag="div", value="Hello, World!", props={"class": "greeting"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.props, {"class": "greeting"})
    

    def test_props_to_html(self):
        node = HtmlNode(tag="div", value="Hello, World!", props={"class": "greeting"})
        self.assertEqual(node.props_to_html(), ' class="greeting"')

    def test_repr(self):
        node = HtmlNode(tag="div", value="Hello, World!", props={"class": "greeting"})
        self.assertEqual(repr(node), 'HtmlNode(tag=div, value=Hello, World!, children=None, props={"class": "greeting"})')
    


if __name__ == '__main__':
    unittest.main()

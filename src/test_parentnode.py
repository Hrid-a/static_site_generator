import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        parent = ParentNode("div", [
            LeafNode("p", "First"),
            LeafNode("p", "Second"),
            LeafNode("p", "Third"),
        ])
        self.assertEqual(
            parent.to_html(),
            "<div><p>First</p><p>Second</p><p>Third</p></div>"
        )

    def test_parentnode_with_props(self):
        parent = ParentNode("div", [LeafNode("span", "child")], {"class": "container"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><span>child</span></div>'
        )

    def test_missing_tag_raises(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("p", "child")])

    def test_missing_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

        with self.assertRaises(ValueError):
            ParentNode("div", [])

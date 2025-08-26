import unittest
from textnode import TextNode, TextType

class testTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode('text', TextType.ITALIC)
        node2 = TextNode('text', TextType.ITALIC)

        self.assertEqual(node, node2)


    def test_not_eq(self):
        node = TextNode('text', TextType.LINK, 'http://localhost:8000')
        node2 = TextNode('text', TextType.IMAGE, 'http://localhost:8000')
        self.assertNotEqual(node, node2)

    def test_link_eq(self):
        node = TextNode('text', TextType.LINK, 'http://localhost:8000')
        node2 = TextNode('text', TextType.LINK, 'http://localhost:8000')
        self.assertEqual(node, node2)



if __name__ == '__main__':
    unittest.main()
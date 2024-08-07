import unittest

from src.textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", "italic", "https://www.boot.dev")
        node2 = TextNode("This is a another text node", "bold", "https://www.boot.dev/blog")
        node3 = TextNode("This is a text node", "italic", "https://www.boot.dev")
        node4 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)
    
    def test_prop_is_none(self):
        node = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertIsNotNone(node.text)
        self.assertIsNotNone(node.text_type)
        self.assertIsNotNone(node.url)

if __name__ == "__main__":
    unittest.main()
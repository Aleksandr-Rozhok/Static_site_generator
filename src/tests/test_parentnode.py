import unittest

from src.htmlnode import ParentNode
from src.htmlnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_case_for_params(self):
        parent_node1 = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"align": "center"}
        )
        parent_node2 = ParentNode(
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"align": "center"}
        )

        self.assertIsInstance(parent_node1.children, list, "Value should be a list")
        self.assertIsInstance(parent_node2.children, list, "Value should be a list")

    def test_default_case(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        expected_result = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        tested_case = parent_node.to_html()
        self.assertEqual(expected_result, tested_case)

    def test_no_children_case(self):
        parent_node = ParentNode("p",[], {"align": "center"})

        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

        self.assertEqual(str(context.exception), "There not a children")

    def test_parent_node_inside_another(self):
        parent_node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ])
            ],
        )

        expected_result = "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>"
        tested_case = parent_node.to_html()
        
        self.assertEqual(expected_result, tested_case)

if __name__ == "__main__":
    unittest.main()
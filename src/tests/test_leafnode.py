import unittest

from src.htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_without_params(self):
        leaf_node = LeafNode("This is a paragraph of text.")

        expected_result = "This is a paragraph of text."
        tested_result = leaf_node.to_html()
        
        self.assertEqual(expected_result, tested_result)
    
    def test_to_html_with_tags(self):
        leaf_node1 = LeafNode("p", "This is a paragraph of text.")
        leaf_node2 = LeafNode("h1", "This is a title of text.")

        expected_result_for_first_node = "<p>This is a paragraph of text.</p>"
        expected_result_for_second_node = "<h1>This is a title of text.</h1>"
        first_test_case = leaf_node1.to_html()
        second_test_case = leaf_node2.to_html()
        
        self.assertEqual(expected_result_for_first_node, first_test_case)
        self.assertEqual(expected_result_for_second_node, second_test_case)
    
    def test_to_html_with_tags(self):
        leaf_node1 = LeafNode("a", "Google.com", {"href": "https://www.google.com"})
        leaf_node2 = LeafNode("a", "Google.com", {"href": "https://www.google.com", "target": "_blank"})

        expected_result_for_first_node = "<a href=\"https://www.google.com\">Google.com</a>"
        expected_result_for_second_node = "<a href=\"https://www.google.com\" target=\"_blank\">Google.com</a>"
        first_test_case = leaf_node1.to_html()
        second_test_case = leaf_node2.to_html()
        
        self.assertEqual(expected_result_for_first_node, first_test_case)
        self.assertEqual(expected_result_for_second_node, second_test_case)

    def test_case_for_params(self):
        leaf_node1 = LeafNode("a", "Some text", {"href": "https://www.google.com"})
        leaf_node2 = LeafNode("p", "This is a paragraph of text.")
        leaf_node3 = LeafNode("Only value")
        leaf_node4 = LeafNode(None, "Normal text")
        leaf_node5 = LeafNode("a", None, {"href": "https://www.google.com"})

        self.assertEqual("Some text", leaf_node1.value)
        self.assertEqual("This is a paragraph of text.", leaf_node2.value)
        self.assertEqual("Only value", leaf_node3.value)
        self.assertEqual("Normal text", leaf_node4.value)
        self.assertEqual(None, leaf_node5.value)
    
    def test_no_value_case(self):
        leaf_node1 = LeafNode("a", None, {"href": "https://www.google.com"})

        with self.assertRaises(ValueError) as context:
            leaf_node1.to_html()

        self.assertEqual(str(context.exception), "All leaf nodes must have a value")
    
    def test_single_tag_case(self):
        leaf_node1 = LeafNode("img", " ", {"src": "https://www.google.com", "alt": "Some alt for img"})
        leaf_node2 = LeafNode("br", " ")

        expected_result_for_first_node = "<img src=\"https://www.google.com\" alt=\"Some alt for img\"/>"
        expected_result_for_second_node = "<br/>"
        first_test_case = leaf_node1.to_html()
        second_test_case = leaf_node2.to_html()
        
        self.assertEqual(expected_result_for_first_node, first_test_case)
        self.assertEqual(expected_result_for_second_node, second_test_case)


if __name__ == "__main__":
    unittest.main()
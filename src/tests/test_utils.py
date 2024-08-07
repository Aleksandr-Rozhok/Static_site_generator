import unittest

from src.textnode import TextNode
from src.utils import split_nodes_delimiter, text_node_to_html_node

class TestUtils(unittest.TestCase):
    def test_func_text_node_to_html_node(self):
        text_node1 = TextNode("This is a text node with type 'text'", "text")
        text_node2 = TextNode("This is a text node with type 'bold'", "bold")
        text_node3 = TextNode("This is a text node with type 'italic'", "italic")
        text_node4 = TextNode("This is a text node with type 'code'", "code")
        text_node5 = TextNode("This is a text node with type 'link'", "link", "https://www.boot.dev")
        text_node6 = TextNode("This is a text node with type 'image'", "image", "images/sample.gif")

        test_case1 = text_node_to_html_node(text_node1).to_html()
        test_case2 = text_node_to_html_node(text_node2).to_html()
        test_case3 = text_node_to_html_node(text_node3).to_html()
        test_case4 = text_node_to_html_node(text_node4).to_html()
        test_case5 = text_node_to_html_node(text_node5).to_html()
        test_case6 = text_node_to_html_node(text_node6).to_html()

        expected_result1 = "This is a text node with type 'text'"
        expected_result2 = "<b>This is a text node with type 'bold'</b>"
        expected_result3 = "<i>This is a text node with type 'italic'</i>"
        expected_result4 = "<code>This is a text node with type 'code'</code>"
        expected_result5 = "<a href=\"https://www.boot.dev\">This is a text node with type 'link'</a>"
        expected_result6 = "<img src=\"images/sample.gif\" alt=\"This is a text node with type 'image'\"/>"

        self.assertEqual(test_case1, expected_result1)
        self.assertEqual(test_case2, expected_result2)
        self.assertEqual(test_case3, expected_result3)
        self.assertEqual(test_case4, expected_result4)
        self.assertEqual(test_case5, expected_result5)
        self.assertEqual(test_case6, expected_result6)
    
    def test_func_without_unknown_type(self):
        text_node1 = TextNode("This is a text node with type 'text'", "circle")

        with self.assertRaises(TypeError) as context:
            text_node_to_html_node(text_node1)

        self.assertEqual(str(context.exception), "There no your type of text")

    def test_split_nodes_delimiter(self):
        text_node1 = TextNode("This is text with a `code block` word", "text")
        text_node2 = TextNode("This is text with a `code block` word", "bold")
        text_node3 = TextNode("This is text with a **bold block** word", "text")
        text_node4 = TextNode("This is text with a *italic block* word", "text")
        text_node5 = TextNode("This is text with a *italic block* word, which added *twice*", "text")
        text_node6 = TextNode("This is text with a ```code block``` word", "text")

        excepted_result1 = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        excepted_result2 = [TextNode("This is text with a `code block` word", "bold")]
        excepted_result3 = [
            TextNode("This is text with a ", "text"),
            TextNode("bold block", "bold"),
            TextNode(" word", "text"),
        ]
        excepted_result4 = [
            TextNode("This is text with a ", "text"),
            TextNode("italic block", "italic"),
            TextNode(" word", "text"),
        ]
        excepted_result5 = [
            TextNode("This is text with a ", "text"),
            TextNode("italic block", "italic"),
            TextNode(" word, which added ", "text"),
            TextNode("twice", "italic"),
        ]
        excepted_result6 = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]

        test_case1 = split_nodes_delimiter(text_node1, "`", "code")
        test_case2 = split_nodes_delimiter(text_node2, "`", "code")
        test_case3 = split_nodes_delimiter(text_node3, "**", "bold")
        test_case4 = split_nodes_delimiter(text_node4, "*", "italic")
        test_case5 = split_nodes_delimiter(text_node5, "*", "italic")
        test_case6 = split_nodes_delimiter(text_node6, "```", "code")

        self.assertEqual(excepted_result1, test_case1)  
        self.assertEqual(excepted_result2, test_case2)
        self.assertEqual(excepted_result3, test_case3)
        self.assertEqual(excepted_result4, test_case4)
        self.assertEqual(excepted_result5, test_case5)
        self.assertEqual(excepted_result6, test_case6)
    
    def test_split_nodes_without_delimiter(self):
        text_node1 = TextNode("This is text with a `code block` word", "text")

        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(text_node1, "*", "italic")

        self.assertEqual(str(context.exception), "There is no delimiter in this TextNode")



if __name__ == "__main__":
    unittest.main()
import unittest

from src.textnode import TextNode
from src.utils import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_links, text_node_to_html_node, text_to_textnodes

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
        text_node1 = [TextNode("This is text with a `code block` word", "text")]
        text_node2 = [TextNode("This is text with a `code block` word", "bold")]
        text_node3 = [TextNode("This is text with a **bold block** word", "text")]
        text_node4 = [TextNode("This is text with a *italic block* word", "text")]
        text_node5 = [TextNode("This is text with a *italic block* word, which added *twice*", "text")]
        text_node6 = [TextNode("This is text with a ```code block``` word", "text")]
        text_node7 = [TextNode("```code block``` This is text with a word", "text")]

        expected_result1 = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        expected_result2 = [TextNode("This is text with a `code block` word", "bold")]
        expected_result3 = [
            TextNode("This is text with a ", "text"),
            TextNode("bold block", "bold"),
            TextNode(" word", "text"),
        ]
        expected_result4 = [
            TextNode("This is text with a ", "text"),
            TextNode("italic block", "italic"),
            TextNode(" word", "text"),
        ]
        expected_result5 = [
            TextNode("This is text with a ", "text"),
            TextNode("italic block", "italic"),
            TextNode(" word, which added ", "text"),
            TextNode("twice", "italic"),
        ]
        expected_result6 = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ]
        expected_result7 = [
            TextNode("code block", "code"),
            TextNode(" This is text with a word", "text"),
        ]

        test_case1 = split_nodes_delimiter(text_node1, "`", "code")
        test_case2 = split_nodes_delimiter(text_node2, "`", "code")
        test_case3 = split_nodes_delimiter(text_node3, "**", "bold")
        test_case4 = split_nodes_delimiter(text_node4, "*", "italic")
        test_case5 = split_nodes_delimiter(text_node5, "*", "italic")
        test_case6 = split_nodes_delimiter(text_node6, "```", "code")
        test_case7 = split_nodes_delimiter(text_node7, "```", "code")

        self.assertEqual(expected_result1, test_case1)  
        self.assertEqual(expected_result2, test_case2)
        self.assertEqual(expected_result3, test_case3)
        self.assertEqual(expected_result4, test_case4)
        self.assertEqual(expected_result5, test_case5)
        self.assertEqual(expected_result6, test_case6)
        self.assertEqual(expected_result7, test_case7)
    
    def test_split_nodes_without_delimiter(self):
        text_node1 = [TextNode("This is text with a `code block` word", "text")]

        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter(text_node1, "^", "italic")

        self.assertEqual(str(context.exception), "There is no ^ delimiter")

    def test_extract_markdown_images(self):
        text1 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        text2 = "This is text with a ![dart maul](https://vk.ru/aKaOqIh.png) and ![obi wan](https://pinterest.com/fJRm4Vk.jpeg)"
        text3 = "This is text with a ![dart maul](https://vk.ru/aKaOqIh.png) and it's all"

        test_case1 = extract_markdown_images(text1)
        test_case2 = extract_markdown_images(text2)
        test_case3 = extract_markdown_images(text3)
        
        expected_result1 = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        expected_result2 = [("dart maul", "https://vk.ru/aKaOqIh.png"), ("obi wan", "https://pinterest.com/fJRm4Vk.jpeg")]
        expected_result3 = [("dart maul", "https://vk.ru/aKaOqIh.png")]

        self.assertEqual(expected_result1, test_case1) 
        self.assertEqual(expected_result2, test_case2)
        self.assertEqual(expected_result3, test_case3)
    
    def test_extract_markdown_links(self):
        text1 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        text2 = "This is text with a link [to boot dev](https://www.boot.dev)"

        test_case1 = extract_markdown_links(text1)
        test_case2 = extract_markdown_links(text2)
        
        expected_result1 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        expected_result2 = [("to boot dev", "https://www.boot.dev")]

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2) 

    def test_split_node_links(self):
        text_node1 = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        "text")
        text_node2 = TextNode(
        "[to boot dev](https://www.boot.dev) This is text with a link and [to youtube](https://www.youtube.com/@bootdotdev)",
        "text")
        text_node3 = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev), so it's all",
        "text")
        text_node4 = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev), so it's all",
        "bold")

        test_case1 = split_nodes_links([text_node1])
        test_case2 = split_nodes_links([text_node2])
        test_case3 = split_nodes_links([text_node3])
        test_case4 = split_nodes_links([text_node4])

        expected_result1 = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" and ", "text"),
            TextNode(
                "to youtube", "link", "https://www.youtube.com/@bootdotdev"
            ),
        ]
        expected_result2 = [
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(" This is text with a link and ", "text"),
            TextNode(
                "to youtube", "link", "https://www.youtube.com/@bootdotdev"
            ),
        ]
        expected_result3 = [
            TextNode("This is text with a link ", "text"),
            TextNode("to boot dev", "link", "https://www.boot.dev"),
            TextNode(", so it's all", "text"),
        ]
        expected_result4 = [
            TextNode(
                "This is text with a link [to boot dev](https://www.boot.dev), so it's all",
                "bold")
        ]

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2)
        self.assertEqual(expected_result3, test_case3)
        self.assertEqual(expected_result4, test_case4)

    def test_split_nodes_image(self):
        text_node1 = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            "text")
        text_node2 = TextNode(
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) This is text with a img ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            "text")
        text_node3 = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and it's all",
            "text")
        text_node4 = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and it's all",
            "bold")
        
        test_case1 = split_nodes_image([text_node1])
        test_case2 = split_nodes_image([text_node2])
        test_case3 = split_nodes_image([text_node3])
        test_case4 = split_nodes_image([text_node4])

        expected_result1 = [
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "img", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", "text"),
            TextNode(
                "obi wan", "img", "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        expected_result2 = [
            TextNode("rick roll", "img", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" This is text with a img ", "text"),
            TextNode(
                "obi wan", "img", "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        expected_result3 = [
            TextNode("This is text with a ", "text"),
            TextNode("rick roll", "img", "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and it's all", "text"),
        ]
        expected_result4 = [
            TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and it's all",
            "bold")
        ]

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2)
        self.assertEqual(expected_result3, test_case3)
        self.assertEqual(expected_result4, test_case4)

    def test_text_to_textnodes(self):
        text1 = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text2 = ""

        test_case1 = text_to_textnodes(text1)
        test_case2 = text_to_textnodes(text2)

        expected_result1 = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "img", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        expected_result2 = []

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2)

if __name__ == "__main__":
    unittest.main()
import unittest

from src.textnode import TextNode
from src.htmlnode import HTMLNode
from src.utils import (
    extract_markdown_images, 
    extract_markdown_links, 
    markdown_to_blocks, 
    split_nodes_delimiter, 
    split_nodes_image, 
    split_nodes_links, 
    text_node_to_html_node, 
    text_to_textnodes, 
    block_to_block_type, 
    markdown_to_html_node,
    heading_to_htmlnode,
    any_type_to_htmlnode,
    list_to_htmlnode
    )

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
    
    def test_markdown_to_blocks(self):
        text1 = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""
        
        text2 = """### This is also heading

        1. This is first element of list
        2. This is second element of list
        3. This is third element of list

        The end of markdown document."""

        text3 = ""

        test_case1 = markdown_to_blocks(text1)
        test_case2 = markdown_to_blocks(text2)
        test_case3 = markdown_to_blocks(text3)

        expected_result1 = ["# This is a heading\n", 
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n", 
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item\n"]
        expected_result2 = ["### This is also heading\n", 
            "1. This is first element of list\n2. This is second element of list\n3. This is third element of list\n",
            "The end of markdown document.\n"]
        expected_result3 = []

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2)
        self.assertEqual(expected_result3, test_case3)
    
    def test_block_to_block_type(self):
        text1 = "### This is title"
        text2 = "```some code```"
        text3 = "> This is quote"
        text4 = markdown_to_blocks("""* This is the first list item in a list block
        * This is a list item
        * This is another list item""")
        text5 = markdown_to_blocks("""1. This is first element of list
        2. This is second element of list
        3. This is third element of list""")
        text6 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."

        test_case1 = block_to_block_type(text1)
        test_case2 = block_to_block_type(text2)
        test_case3 = block_to_block_type(text3)
        test_case4 = block_to_block_type(text4[0])
        test_case5 = block_to_block_type(text5[0])
        test_case6 = block_to_block_type(text6)

        expected_result1 = "heading"
        expected_result2 = "code"
        expected_result3 = "quote"
        expected_result4 = "unordered_list"
        expected_result5 = "ordered_list"
        expected_result6 = "paragraph"

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2)
        self.assertEqual(expected_result3, test_case3)
        self.assertEqual(expected_result4, test_case4)
        self.assertEqual(expected_result5, test_case5)
        self.assertEqual(expected_result6, test_case6)

    def test_every_line_in_block_type(self):
        text1 = """> This is quote
        > This is too quote
        And this isn't a quote"""
        text2 = """* This is the first list item in a list block
        - This is a list item
        . This is another list item"""
        text3 = """1. This is first element of list
        2. This is second element of list
        4. This is third element of list"""

        with self.assertRaises(ValueError) as context:
            block_to_block_type(text1)

        self.assertEqual(str(context.exception), "Every line must be a quote")

        with self.assertRaises(ValueError) as context:
            block_to_block_type(text2)

        self.assertEqual(str(context.exception), "Every line must be an item of unordered list")

        with self.assertRaises(ValueError) as context:
            block_to_block_type(text3)

        self.assertEqual(str(context.exception), "Every line must be an item of ordered list")
    
    def test_markdown_to_html_node(self):
        text1 = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item"""

        text2 = """## This is a small heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        Also, we have a ```code```

        1. This is the first list item in ordered list
        2. This is a second list item in ordered list
        3. This is another list item in ordered list"""

        test_case1 = markdown_to_html_node(text1)
        test_case2 = markdown_to_html_node(text2)

        expected_result1 = HTMLNode("div", None, [
            HTMLNode("h1", "This is a heading", None, None), 
            HTMLNode("p", "This is a paragraph of text. It has some  and  words inside of it.", [
                HTMLNode("b", "bold", None, None), 
                HTMLNode("i", "italic", None, None)
            ], None), 
            HTMLNode("ul", None, [
                HTMLNode("li", "This is the first list item in a list block", None, None), 
                HTMLNode("li", "This is a list item", None, None), 
                HTMLNode("li", "This is another list item", None, None)
            ], None)
        ], None)

        expected_result2 = HTMLNode("div", None, [
            HTMLNode("h2", "This is a small heading", None, None), 
            HTMLNode("p", "This is a paragraph of text. It has some  and  words inside of it.", [
                HTMLNode("b", "bold", None, None), 
                HTMLNode("i", "italic", None, None)
            ], None),
            HTMLNode("p", "Also, we have a ", [
                HTMLNode("code", "code", None, None)
            ], None), 
            HTMLNode("ol", None, [
                HTMLNode("li", "This is the first list item in ordered list", None, None), 
                HTMLNode("li", "This is a second list item in ordered list", None, None), 
                HTMLNode("li", "This is another list item in ordered list", None, None)
            ], None)
        ], None)

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2)
    
    def test_heading_to_htmlnode(self):
        text1 = "# First Title"
        text2 = "## Second Title"
        text3 = "###### Third Title"
        text4 = "################### Non-existent title"
        text5 = "Just text"

        test_case1 = heading_to_htmlnode(text1)
        test_case2 = heading_to_htmlnode(text2)
        test_case3 = heading_to_htmlnode(text3)

        expected_result1 = HTMLNode("h1", "First Title", None, None)
        expected_result2 = HTMLNode("h2", "Second Title", None, None)
        expected_result3 = HTMLNode("h6", "Third Title", None, None)

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2)
        self.assertEqual(expected_result3, test_case3)

        with self.assertRaises(ValueError) as context:
            heading_to_htmlnode(text4)

        self.assertEqual(str(context.exception), "Incorrect title")

        with self.assertRaises(ValueError) as context:
            heading_to_htmlnode(text5)

        self.assertEqual(str(context.exception), "Incorrect title")

    def test_any_type_to_htmlnode(self):
        text1 = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        text2 = "This is a paragraph of text. Without any children"

        test_case1 = any_type_to_htmlnode(text1, "p")
        test_case2 = any_type_to_htmlnode(text2, "p")

        expected_result1 = HTMLNode("p", "This is a paragraph of text. It has some  and  words inside of it.", [
            HTMLNode("b", "bold", None, None),
            HTMLNode("i", "italic", None, None)
        ], None)
        expected_result2 = HTMLNode("p", "This is a paragraph of text. Without any children", None, None)

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2)

    def test_list_to_htmlnode(self):
        text1 =  """* This is the first list item in a list block
         * This is a list item
         * This is another list item with **bold** element"""
        
        text2 =  """* This is the first list item in a list block
         * This is a list item
         * This is also list item with *italic* and `code`
         * This is another list item with **bold** element"""
        
        text3 =  """1. This is the first list item in a list block
         2. This is a list item
         3. This is also list item with *italic* and `code`
         4. This is another list item with **bold** element"""
        
        text4 =  """1. 1. This is the first list item in a list block
         2. 2. This is a list item
         3. 3. This is also list item with *italic* and `code`
         4. 4. This is another list item with **bold** element"""
        
        test_case1 = list_to_htmlnode(text1, "ul")
        test_case2 = list_to_htmlnode(text2, "ul")
        test_case3 = list_to_htmlnode(text3, "ol")
        test_case4 = list_to_htmlnode(text4, "ol")

        expected_result1 = HTMLNode("ul", None, [
            HTMLNode("li", "This is the first list item in a list block", None, None),
            HTMLNode("li", "This is a list item", None, None),
            HTMLNode("li", "This is another list item with  element", [
                HTMLNode("b", "bold", None, None),
            ], None),
        ], None)

        expected_result2 = HTMLNode("ul", None, [
            HTMLNode("li", "This is the first list item in a list block", None, None),
            HTMLNode("li", "This is a list item", None, None),
            HTMLNode("li", "This is also list item with  and ", [
                HTMLNode("i", "italic", None, None),
                HTMLNode("code", "code", None, None),
            ], None),
            HTMLNode("li", "This is another list item with  element", [
                HTMLNode("b", "bold", None, None),
            ], None),
        ], None)

        expected_result3 = HTMLNode("ol", None, [
            HTMLNode("li", "This is the first list item in a list block", None, None),
            HTMLNode("li", "This is a list item", None, None),
            HTMLNode("li", "This is also list item with  and ", [
                HTMLNode("i", "italic", None, None),
                HTMLNode("code", "code", None, None),
            ], None),
            HTMLNode("li", "This is another list item with  element", [
                HTMLNode("b", "bold", None, None),
            ], None),
        ], None)

        expected_result4 = HTMLNode("ol", None, [
            HTMLNode("li", "1. This is the first list item in a list block", None, None),
            HTMLNode("li", "2. This is a list item", None, None),
            HTMLNode("li", "3. This is also list item with  and ", [
                HTMLNode("i", "italic", None, None),
                HTMLNode("code", "code", None, None),
            ], None),
            HTMLNode("li", "4. This is another list item with  element", [
                HTMLNode("b", "bold", None, None),
            ], None),
        ], None)

        self.assertEqual(expected_result1, test_case1)
        self.assertEqual(expected_result2, test_case2)
        self.assertEqual(expected_result3, test_case3)
        self.assertEqual(expected_result4, test_case4)


if __name__ == "__main__":
    unittest.main()
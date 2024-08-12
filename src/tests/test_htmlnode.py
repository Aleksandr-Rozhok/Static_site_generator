import unittest

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("h1", "Some Paragraph", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })

        expected_result = 'href="https://www.google.com" target="_blank"'
        tested_result = node.props_to_html()
        
        self.assertEqual(expected_result, tested_result)
    
    def test_props_to_html_with_diff(self):
        node = HTMLNode("h1", "Some Paragraph", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })

        expected_result = 'href=https://www.google.com target=_blank'
        tested_result = node.props_to_html()
        
        self.assertNotEqual(expected_result, tested_result)
    
    def test_is_none(self):
        node = HTMLNode("h1", "Some Paragraph", None, None)

        expected_result = ""
        tested_result = node.props_to_html()
        
        self.assertEqual(expected_result, tested_result)
    
    def test_eq(self):
        node = HTMLNode("h1", "Some Title", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })

        node2 = HTMLNode("h1", "Some Title", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })

        node3 = HTMLNode("h1", "Some Title", [HTMLNode("h2", "Next Title", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })], {
            "href": "https://www.google.com", 
            "target": "_blank",
        })

        node4 = HTMLNode("h1", "Some Title", [HTMLNode("h2", "Next Title", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })], {
            "href": "https://www.google.com", 
            "target": "_blank",
        })

        node5 = HTMLNode("div", None, [
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

        node6 = HTMLNode("div", None, [
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

        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertEqual(node5, node6)
    
    def test_not_eq(self):
        node = HTMLNode("h1", "Some Title", [HTMLNode("h2", "Some Paragraph !", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })], {
            "href": "https://www.facebook.com", 
            "target": "_blank",
        })

        node2 = HTMLNode("h1", "Some Title", [HTMLNode("h1", "Some Paragraph", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })], {
            "href": "https://www.google.com", 
            "target": "_blank",
        })

        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
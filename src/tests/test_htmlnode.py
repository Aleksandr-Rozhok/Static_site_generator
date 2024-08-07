import unittest

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "Some Paragraph", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })

        expected_result = 'href="https://www.google.com" target="_blank"'
        tested_result = node.props_to_html()
        
        self.assertEqual(expected_result, tested_result)
    
    def test_not_eq(self):
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

if __name__ == "__main__":
    unittest.main()
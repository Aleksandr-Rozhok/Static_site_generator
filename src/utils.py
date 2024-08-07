from src.htmlnode import LeafNode
from enum import Enum

from src.textnode import TextNode

class TextTypeNode(Enum):
        text_type_text = "text"
        text_type_bold = "bold"
        text_type_italic = "italic"
        text_type_code = "code"
        text_type_link = "link"
        text_type_image = "image"

        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)

def text_node_to_html_node(text_node):  
    if text_node.text_type == TextTypeNode.text_type_text.value:
        return LeafNode(text_node.text)
    elif text_node.text_type == TextTypeNode.text_type_bold.value:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextTypeNode.text_type_italic.value:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextTypeNode.text_type_code.value:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextTypeNode.text_type_link.value:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextTypeNode.text_type_image.value:
        return LeafNode("img", " ", {"src": text_node.url, "alt": text_node.text})
    elif not TextTypeNode.has_value(text_node.text_type):
        raise TypeError("There no your type of text")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if old_nodes.text_type != TextTypeNode.text_type_text.value:
        return [old_nodes]
    elif delimiter not in old_nodes.text:
        raise ValueError("There is no delimiter in this TextNode")
    else:
        list_of_substr = old_nodes.text.split(delimiter)
        if list_of_substr[-1] == "":
            list_of_substr.pop()
  
        result = []

        for index in range(0, len(list_of_substr)):
            if index % 2 == 0:
                result.append(TextNode(list_of_substr[index], "text"))
            else:
                result.append(TextNode(list_of_substr[index], text_type))
        
        return result
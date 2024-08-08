import math
from src.htmlnode import LeafNode
from enum import Enum
import re

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
    for old_node in old_nodes:
        if old_node.text_type != TextTypeNode.text_type_text.value:
            return [old_node]
        elif delimiter not in old_node.text:
            raise ValueError("There is no delimiter in this TextNode")
        else:
            list_of_substr = old_node.text.split(delimiter)
            if list_of_substr[-1] == "":
                list_of_substr.pop()
    
            result = []

            for index in range(0, len(list_of_substr)):
                if index % 2 == 0:
                    if list_of_substr[index] == "":
                        pass
                    else:
                        result.append(TextNode(list_of_substr[index], "text"))
                else:
                    result.append(TextNode(list_of_substr[index], text_type))
            
            return result
    
def extract_markdown_images(text):
    matches_alt_img = re.findall(r"!\[(.*?)\]", text)
    matches_href_img = re.findall(r"https:\/\/[^\s\/$.?#].[^\s\)]*", text)
    result = []

    if not matches_alt_img and not matches_href_img:
        raise ValueError("There is no images here")

    for index in range(0, len(matches_alt_img)):
        result.append((matches_alt_img[index], matches_href_img[index]))

    return result

def extract_markdown_links(text):
    matches_url_text = re.findall(r"\[(.*?)\]", text)
    matches_url = re.findall(r"https:\/\/[^\s\/$.?#].[^\s\)]*", text)
    result = []

    if not matches_url_text and not matches_url:
        raise ValueError("There is no links here")

    for index in range(0, len(matches_url_text)):
        result.append((matches_url_text[index], matches_url[index]))

    return result

def split_nodes_links(old_nodes):
    for old_node in old_nodes:
        if old_node.text_type != TextTypeNode.text_type_text.value:
            return [old_node]
        else:
            arg_text = old_node.text
            extracted_links = extract_markdown_links(old_node.text)
            result = []
            text_count = 0
            links_count = 0
            
            for link in extracted_links:
                arg_text = "".join(arg_text.split(link[0]))
                arg_text = "".join(arg_text.split(link[1]))
            
            list_of_only_text = arg_text.split("[]()")

            if list_of_only_text[-1] == "":
                list_of_only_text.pop()

            for index in range(0, len(list_of_only_text) + len(extracted_links)):
                if index % 2 == 0:
                    if list_of_only_text[text_count] == "":
                        text_count += 1
                    else:
                        result.append(TextNode(list_of_only_text[text_count], "text"))
                        text_count += 1
                else:
                    result.append(TextNode(extracted_links[links_count][0], "link", extracted_links[links_count][1]))
                    links_count += 1
            
            return result
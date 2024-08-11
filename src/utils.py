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
    result = []
    all_delimiters = ["*", "**", "`", "```"]
    
    if delimiter not in all_delimiters:
        raise ValueError(f"There is no {delimiter} delimiter")

    for old_node in old_nodes:
        if old_node.text_type != TextTypeNode.text_type_text.value:
            result.append(old_node)
        else:
            list_of_substr = old_node.text.split(delimiter)
            if list_of_substr[-1] == "":
                list_of_substr.pop()

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

    for index in range(0, len(matches_alt_img)):
        result.append((matches_alt_img[index], matches_href_img[index]))

    return result

def extract_markdown_links(text):
    matches_url_text = re.findall(r"\[(.*?)\]", text)
    matches_url = re.findall(r"https:\/\/[^\s\/$.?#].[^\s\)]*", text)
    result = []

    for index in range(0, len(matches_url_text)):
        result.append((matches_url_text[index], matches_url[index]))

    return result

def split_nodes_links(old_nodes):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextTypeNode.text_type_text.value:
            result.append(old_node)
        else:
            arg_text = old_node.text
            extracted_links = extract_markdown_links(old_node.text)
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

def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextTypeNode.text_type_text.value:
            result.append(old_node)
        else:
            arg_text = old_node.text
            extracted_img = extract_markdown_images(old_node.text)
            text_count = 0
            img_count = 0
            
            for img in extracted_img:
                arg_text = "".join(arg_text.split(img[0]))
                arg_text = "".join(arg_text.split(img[1]))
            
            list_of_only_text = arg_text.split("![]()")

            if list_of_only_text[-1] == "":
                list_of_only_text.pop()

            for index in range(0, len(list_of_only_text) + len(extracted_img)):
                if index % 2 == 0:
                    if list_of_only_text[text_count] == "":
                        text_count += 1
                    else:
                        result.append(TextNode(list_of_only_text[text_count], "text"))
                        text_count += 1
                else:
                    result.append(TextNode(extracted_img[img_count][0], "img", extracted_img[img_count][1]))
                    img_count += 1
            
    return result

def text_to_textnodes(text):
    new_text_node = TextNode(text, TextTypeNode.text_type_text.value)
    nodes_with_code = split_nodes_delimiter([new_text_node], "`", TextTypeNode.text_type_code.value)
    nodes_with_bold_text = split_nodes_delimiter(nodes_with_code, "**", TextTypeNode.text_type_bold.value)
    nodes_with_italic_text = split_nodes_delimiter(nodes_with_bold_text, "*", TextTypeNode.text_type_italic.value)
    nodes_with_img = split_nodes_image(nodes_with_italic_text)
    totally_divided_nodes = split_nodes_links(nodes_with_img)
    
    return totally_divided_nodes

def markdown_to_blocks(markdown):
    result = []
    temp_line = ""

    if not markdown:
        return result

    divided_markdown = markdown.split("\n") 

    for line in divided_markdown:
        if line == "":
            result.append(temp_line)
            temp_line = ""
        else:
            temp_line += line.strip() + "\n"

    result.append(temp_line)
    return result

def block_to_block_type(markdown_block):
    divided_markdown_block = markdown_block.split("\n")
    if divided_markdown_block[-1] == "":
        divided_markdown_block.pop()

    if "#" in divided_markdown_block[0][0]:
        return "heading"
    elif divided_markdown_block[0][0:3] == "```":
        return "code"
    elif divided_markdown_block[0][0] == ">":
        for line in divided_markdown_block:
            line.strip()
            if line[0] != ">":
                raise ValueError("Every line must be a quote")
            
        return "quote"
    elif divided_markdown_block[0][0] == "*" or divided_markdown_block[0][0] == "-":
        for line in divided_markdown_block:
            line.strip()
            if line[0] != "*" and line[0] != "-":
                raise ValueError("Every line must be an item of unordered list")
            
        return "unordered_list"
    elif divided_markdown_block[0][0:2] == "1.":
        for index in range(len(divided_markdown_block)):
            divided_markdown_block[index].strip()
            if divided_markdown_block[index][0] != str(index + 1):
                raise ValueError("Every line must be an item of ordered list")
            
        return "ordered_list"
    else:
        return "paragraph"
    
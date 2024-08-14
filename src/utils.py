from src.htmlnode import LeafNode, ParentNode
from src.htmlnode import HTMLNode
from src.textnode import TextNode
from enum import Enum
import re

class TextTypeNode(Enum):
        text_type_text = "text"
        text_type_bold = "bold"
        text_type_italic = "italic"
        text_type_code = "code"
        text_type_link = "link"
        text_type_image = "img"

        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)

def text_node_to_leaf_node(text_node):
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
        raise TypeError(f"There no your type of text")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    all_delimiters = ["*", "**", "`", "```", ">"]
    
    if delimiter not in all_delimiters:
        raise ValueError(f"There is no {delimiter} delimiter")

    for old_node in old_nodes:
        if old_node.text_type != TextTypeNode.text_type_text.value:
            result.append(old_node)
        else:
            if delimiter == "*":
                list_of_substr = re.split(r'(?<!^)\*', old_node.text)
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
    matches_href_img = re.findall(r"https?:\/\/[^\s\(\)]+|\/[^\s\(\)]*|\/", text)
    result = []

    for index in range(0, len(matches_alt_img)):
        result.append((matches_alt_img[index], matches_href_img[index]))

    return result

def extract_markdown_links(text):
    matches_url_text = re.findall(r"\[(.*?)\]", text)
    matches_url = re.findall(r"https?:\/\/[^\s\(\)]+|\/[^\s\(\)]*|\/", text)
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
    nodes_with_code1 = split_nodes_delimiter([new_text_node], "```", TextTypeNode.text_type_code.value)
    nodes_with_code2 = split_nodes_delimiter(nodes_with_code1, "`", TextTypeNode.text_type_code.value)
    nodes_with_bold_text = split_nodes_delimiter(nodes_with_code2, "**", TextTypeNode.text_type_bold.value)
    nodes_with_italic_text = split_nodes_delimiter(nodes_with_bold_text, "*", TextTypeNode.text_type_italic.value)
    nodes_with_img = split_nodes_image(nodes_with_italic_text)
    totally_divided_nodes = split_nodes_links(nodes_with_img)
    
    return totally_divided_nodes

def markdown_to_blocks(markdown):
    if not markdown:
        return []
    
    blocks = re.split(r'\n\s*\n', markdown)
    cleared_list_of_blocks = []
    temp_str = ""

    for block in blocks:
        if block.strip("\n ").startswith("*") or block.strip("\n ").startswith("1."):
            list_of_list = block.split("\n")

            for item in list_of_list:
                temp_str += item.strip() + "\n"

            cleared_list_of_blocks.append(temp_str)
            temp_str = ""
        else:
            cleared_list_of_blocks.append(block.strip() + "\n")

    return cleared_list_of_blocks

def block_to_block_type(markdown_block):
    if isinstance(markdown_block, str):
        divided_markdown_block = markdown_block.split("\n")
        cleaned_list = list(filter(lambda x: x != "", divided_markdown_block))
    else:
        cleaned_list = list(filter(lambda x: x != "", markdown_block))
    
    if not cleaned_list:
        return

    if "#" in cleaned_list[0][0]:
        return "heading"
    elif cleaned_list[0][0:3] == "```":
        return "code"
    elif cleaned_list[0][0] == ">":
        for line in cleaned_list:
            line = line.strip()
            if line[0] != ">":
                raise ValueError("Every line must be a quote")
            
        return "quote"
    elif cleaned_list[0][0] == "*" and cleaned_list[0][1] != "*" or cleaned_list[0][0] == "-" and cleaned_list[0][1] != "-":
        for line in cleaned_list:
            line = line.strip()
            if line[0] != "*" and line[0] != "-":
                raise ValueError("Every line must be an item of unordered list")
            
        return "unordered_list"
    elif cleaned_list[0][0:2] == "1.":
        for index in range(len(cleaned_list)):
            cleaned_list[index].strip()
            if cleaned_list[index][0] != str(index + 1):
                raise ValueError("Every line must be an item of ordered list")
            
        return "ordered_list"
    else:
        return "paragraph"
    
def heading_to_htmlnode(text):
        leading_symbols = ""
        heading_text = ""

        match = re.match(r'^([^\w\s]+)(.*)', text)
        if match:
            leading_symbols = match.group(1)
            heading_text = match.group(2).strip()
        else:
            leading_symbols = ''
            heading_text = text.strip()

        if len(leading_symbols) > 6 or len(leading_symbols) == 0:
            raise ValueError("Incorrect title")
        else:
            return any_type_to_parentnode(heading_text, f"h{len(leading_symbols)}")

def blockquote_to_htmlnode(text):
    if text[:2] == "> ":
        return ParentNode("blockquote", [
            LeafNode(text[2:].strip())
        ])
    else:
        raise ValueError("Incorrect quote")


def any_type_to_parentnode(text, our_type):
    list_of_textnodes = text_to_textnodes(text)
    result = ParentNode(our_type, [], None)

    for item in list_of_textnodes:
        item_to_leaf_node = text_node_to_leaf_node(item)
        if not item_to_leaf_node.tag:
            result.children.append(LeafNode(item_to_leaf_node.value, item_to_leaf_node.props))
        else:
            result.children.append(ParentNode(item_to_leaf_node.tag, [LeafNode(item_to_leaf_node.value)], item_to_leaf_node.props))
  
    return result

def list_to_parentnode(text, list_type):
    list_of_textnodes = text.split("\n")
    result = ParentNode(list_type, [], None)

    for item in list_of_textnodes:
        if item == "":
            pass
        else:
            prepared_item = ""
            if list_type == "ul":
                prepared_item = re.sub(r'^[\*\-]\s', '', item.strip(), count=1)
            else:
                prepared_item = re.sub(r'^\d+\.\s', '', item.strip(), count=1)

            result.children.append(any_type_to_parentnode(prepared_item, "li"))

    if not result.children:
        result.children = None
    if not result.value:
        result.value = None

    return result

def markdown_to_html_node(markdown):
    splitted_doc = markdown_to_blocks(markdown)
    result = ParentNode("div", [], None)

    for item in splitted_doc:
        type_of_item = block_to_block_type(item)

        if type_of_item == "heading":
            result.children.append(heading_to_htmlnode(item))
        elif type_of_item == "paragraph":
            result.children.append(any_type_to_parentnode(item, "p"))
        elif type_of_item == "code":
            result.children.append(ParentNode("pre", [
                LeafNode(item, None, None)
            ], None))
        elif type_of_item == "quote":
            result.children.append(blockquote_to_htmlnode(item))
        elif type_of_item == "unordered_list":
            result.children.append(list_to_parentnode(item, "ul"))
        elif type_of_item == "ordered_list":
            result.children.append(list_to_parentnode(item, "ol"))


    return result

def extract_title(markdown):
    leading_symbols = ""
    heading_text = ""

    match = re.match(r'^([^\w\s]+)(.*)', markdown)
    if match:
        leading_symbols = match.group(1)
        heading_text = match.group(2).strip()
    else:
        leading_symbols = ''
        heading_text = markdown.strip()

    if len(leading_symbols) > 1 or len(leading_symbols) == 0:
        raise ValueError("Incorrect title")
    else:
        return heading_text
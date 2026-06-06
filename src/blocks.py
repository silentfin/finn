import re
from enum import Enum

from htmlnode import ParentNode
from inline import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    return list(data.strip() for data in markdown.split("\n\n") if data.strip())


def block_to_block_type(markdown_block) -> BlockType:
    if re.findall(r"^(#{1,6} )", markdown_block):
        return BlockType.HEADING
    elif markdown_block.split("\n")[0].startswith("```") and markdown_block.split("\n")[
        -1
    ].endswith("```"):
        return BlockType.CODE
    elif all(re.findall(r"^> ?", block) for block in markdown_block.split("\n")):
        return BlockType.QUOTE
    elif all(re.findall(r"^- ", block) for block in markdown_block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(
        block.startswith(f"{index + 1}. ")
        for index, block in enumerate(markdown_block.split("\n"))
    ):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.ORDERED_LIST:
        li_items = []
        for line in block.split("\n"):
            children = text_to_children(line.split(". ")[-1])
            li_items.append(ParentNode("li", children))
        ol_node = ParentNode("ol", li_items)
        return ol_node
    elif block_type == BlockType.UNORDERED_LIST:
        li_items = []
        for line in block.split("\n"):
            children = text_to_children(line[2:])
            li_items.append(ParentNode("li", children))
        ul_node = ParentNode("ul", li_items)
        return ul_node
    elif block_type == BlockType.QUOTE:
        quote = " ".join(line[1:].strip() for line in block.split("\n"))
        children = text_to_children(quote)
        quotes = ParentNode("blockquote", children)
        return quotes
    elif block_type == BlockType.CODE:
        content = "\n".join(line.strip() for line in block[4:-3].split("\n"))
        children = text_node_to_html_node(TextNode(content, TextType.TEXT))
        code = ParentNode("code", [children])
        pre_tag = ParentNode("pre", [code])
        return pre_tag
    elif block_type == BlockType.PARAGRAPH:
        para = " ".join(line.strip() for line in block.split("\n"))
        children = text_to_children(para)
        paragraph = ParentNode("p", children)
        return paragraph
    elif block_type == BlockType.HEADING:
        heading_level = 0
        for char in block:
            if char == "#":
                heading_level += 1
            else:
                break
        heading_text = block[heading_level + 1 :]
        children = text_to_children(heading_text)
        heading = ParentNode(f"h{heading_level}", children)
        return heading


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

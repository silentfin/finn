import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            result.append(node)
            continue
        splitted_node = node.text.split(delimiter)
        if len(splitted_node) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        for i in range(len(splitted_node)):
            if splitted_node[i] == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(splitted_node[i], TextType.TEXT))
            else:
                result.append(TextNode(splitted_node[i], text_type))
    return result


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        current_text = node.text
        images = extract_markdown_images(node.text)
        if node.text_type is not TextType.TEXT:
            result.append(node)
            continue
        if len(images) == 0:
            result.append(node)
            continue
        for image in images:
            splitted_text = current_text.split(f"![{image[0]}]({image[1]})", 1)
            if splitted_text[0] != "":
                result.append(TextNode(splitted_text[0], TextType.TEXT))
            result.append(
                TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1])
            )
            current_text = splitted_text[1]
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))
    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        current_text = node.text
        links = extract_markdown_links(node.text)
        if node.text_type is not TextType.TEXT:
            result.append(node)
            continue
        if len(links) == 0:
            result.append(node)
            continue
        for link in links:
            splitted_text = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if splitted_text[0] != "":
                result.append(TextNode(splitted_text[0], TextType.TEXT))
            result.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))
            current_text = splitted_text[1]
        if current_text:
            result.append(TextNode(current_text, TextType.TEXT))
    return result


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

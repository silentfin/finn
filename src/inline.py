from textnode import TextNode, TextType


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

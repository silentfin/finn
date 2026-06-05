import unittest

from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestInline(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_italics(self):
        node = TextNode("This is text with a _italics_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italics", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("**bold** word at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" word at start", TextType.TEXT),
            ],
        )

    def test_already_bold(self):
        node = TextNode("already very bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("already very bold", TextType.BOLD),
            ],
        )

    def test_invalid_markdown(self):
        node = TextNode("This is text with a **unclosed_bold word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_multiple_bolds(self):
        node = TextNode(
            "I am **first bold** and i am **second bold** word", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("I am ", TextType.TEXT),
                TextNode("first bold", TextType.BOLD),
                TextNode(" and i am ", TextType.TEXT),
                TextNode("second bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_mixed_nodes(self):
        nodes = [
            TextNode("This is `code` here", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("another `snippet` text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("another ", TextType.TEXT),
                TextNode("snippet", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [batman](https://batman.com)"
        )
        self.assertListEqual([("batman", "https://batman.com")], matches)

    def test_extract_only_links(self):
        matches = extract_markdown_links(
            "This is text with a [batman](https://batman.com) and here is a cool ![wallpaper](https://wallhaven.cc/w/m96d8m)"
        )
        self.assertListEqual([("batman", "https://batman.com")], matches)

    def test_extract_only_images(self):
        matches = extract_markdown_images(
            "This is text with a [batman](https://batman.com) and here is a cool ![wallpaper](https://wallhaven.cc/w/m96d8m)"
        )
        self.assertListEqual([("wallpaper", "https://wallhaven.cc/w/m96d8m")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "These are cool sites [duckduckgo](https://noai.duckduckgo.com/) and another [wallhaven](https://wallhaven.cc/w/m96d8m)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("These are cool sites ", TextType.TEXT),
                TextNode("duckduckgo", TextType.LINK, "https://noai.duckduckgo.com/"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("wallhaven", TextType.LINK, "https://wallhaven.cc/w/m96d8m"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()

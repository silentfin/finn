import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is cool link", TextType.LINK)
        node4 = TextNode("This is cool link", TextType.LINK)
        node5 = TextNode(
            "This is cool link", TextType.IMAGE, "https://noai.duckduckgo.com/"
        )
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertNotEqual(node2, node4)
        self.assertNotEqual(node4, node5)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text</b>")

    def test_italics(self):
        node = TextNode("This is a italics text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.to_html(), "<i>This is a italics text</i>")

    def test_CODE(self):
        node = TextNode("This is a code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.to_html(), "<code>This is a code text</code>")

    def test_link(self):
        node = TextNode("DuckDuckGo", TextType.LINK, url="https://noai.duckduckgo.com/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(
            html_node.to_html(), '<a href="https://noai.duckduckgo.com/">DuckDuckGo</a>'
        )

    def test_image(self):
        node = TextNode("JJK", TextType.IMAGE, url="https://wallhaven.cc/w/mlzoy1")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://wallhaven.cc/w/mlzoy1" alt="JJK"></img>',
        )


if __name__ == "__main__":
    unittest.main()

import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode()
        node2 = HTMLNode(tag="h1", value="i'm batman")
        node3 = HTMLNode(
            props={
                "href": "https://noai.duckduckgo.com",
                "target": "_blank",
            }
        )
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(repr(node2), "HTMLNode(h1, i'm batman, None, None)")
        self.assertEqual(node2.props_to_html(), "")
        self.assertEqual(
            node3.props_to_html(), ' href="https://noai.duckduckgo.com" target="_blank"'
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


if __name__ == "__main__":
    unittest.main()

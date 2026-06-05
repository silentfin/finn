import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()

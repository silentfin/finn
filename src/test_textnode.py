import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()

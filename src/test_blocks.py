import unittest

from src.blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class Blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_leading_blank_lines(self):
        md = """



This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_trailing_blank_lines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items



        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blank_lines_between_blocks(self):
        md = """



This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items



        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_type_para_heading(self):
        md = "# heading 1"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        md = "## heading 2"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        md = "### heading 3"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        md = "#### heading 4"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        md = "##### heading 5"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        md = "###### heading 6"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        md = "####### heading 7"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_type_code(self):
        md = "```\nhello\n```"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)
        md2 = "```\nhello\nworld\n```"
        block_type = block_to_block_type(md2)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_type_quote(self):
        md = "> cool quote"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)
        md2 = ">another cool quote"
        block_type = block_to_block_type(md2)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_type_paragraph(self):
        md = "blah blah blah #cool blah blah"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_type_unordered_list(self):
        md = "- rice\n- very\n- nice"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_type_ordered_list(self):
        md = "1. rice\n2. very\n3. nice"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        md = "3. rice\n2. very\n1. nice"
        block_type = block_to_block_type(md)
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()

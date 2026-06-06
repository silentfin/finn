import unittest

from website import extract_title


class TestTextNode(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# cool site hell yeah"
        title = extract_title(markdown)
        self.assertEqual(title, "cool site hell yeah")

    def test_with_no_title(self):
        markdown = "cool site hell yeah"
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()

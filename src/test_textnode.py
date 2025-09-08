import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)
        
	def test_eq_with_none(self):
		node = TextNode("This is a text node", TextType.BOLD, None)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_ineq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.TEXT)
		self.assertNotEqual(node, node2)

	def test_ineq_text(self):
		node = TextNode("text", TextType.CODE)
		node2 = TextNode("code", TextType.CODE)
		self.assertNotEqual(node, node2)

	def test_diff_urls(self):
		node = TextNode("link", TextType.LINK, "https://google.com")
		node2 = TextNode("link", TextType.LINK, "https://facebook.com")
		self.assertNotEqual(node, node2)

	def test_url_vs_none(self):
		node = TextNode("link", TextType.LINK, "https://google.com")
		node2 = TextNode("link", TextType.LINK)
		self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
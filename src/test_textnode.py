import unittest

from textnode import TextNode, TextType
from helpers import split_nodes_delimiter

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

	def test_split_text_by_code_blocks(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		target = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT),
		]
		self.assertEqual(target, new_nodes)

	def test_do_not_split_text_with_no_delims(self):
		node = TextNode("This is just a plain old text node", TextType.TEXT)
		target = [TextNode("This is just a plain old text node", TextType.TEXT)]
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(target, new_nodes)

	def test_multiple_matched_pairs(self):
		node = TextNode("PRE `FIRST` MID `SECOND` POST", TextType.TEXT)
		target = [
			TextNode("PRE ", TextType.TEXT),
			TextNode("FIRST", TextType.CODE),
			TextNode(" MID ", TextType.TEXT),
			TextNode("SECOND", TextType.CODE),
			TextNode(" POST", TextType.TEXT),
		]
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(target, new_nodes)

	def test_single_code_block(self):
		node = TextNode("`This`", TextType.TEXT)
		target = [TextNode("This", TextType.CODE)]
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(target, new_nodes)

	def test_start_code_block(self):
		node = TextNode("`This` is a test with a code block", TextType.TEXT)
		target = [
			TextNode("This", TextType.CODE),
			TextNode(" is a test with a code block", TextType.TEXT)
			]
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(target, new_nodes)

	def test_end_code_block(self):
		node = TextNode("This `is a test with a code block`", TextType.TEXT)
		target = [
			TextNode("This ", TextType.TEXT),
			TextNode("is a test with a code block", TextType.CODE)
			]
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(target, new_nodes)

	def test_mis_matched_delims(self):
		node = TextNode("This `is a test with a code block", TextType.TEXT)
		with self.assertRaises(Exception):
			new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

if __name__ == "__main__":
    unittest.main()
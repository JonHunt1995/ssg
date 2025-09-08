import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
	def test_props_to_html(self):
		target = ' href="https://www.google.com" target="_blank"'
		node = HTMLNode('a', "this is a link", None, {
			"href": "https://www.google.com",
			"target": "_blank",
		})
		actual = node.props_to_html()
		self.assertEqual(target, actual)

	def test_repr(self):
		target = 'HTMLNode(tag=None, value=None, children=None, props=None)'
		node = HTMLNode(None, None, None, None)
		actual = node.__repr__()
		self.assertEqual(target, actual)

	def test_init(self):
		attrs = ['tag', 'value', 'children', 'props']
		target = ["p", "This is a paragraph", None, {"id": "main-paragraph"}]
		node = HTMLNode("p", "This is a paragraph", None, {"id": "main-paragraph"})
		[self.assertEqual(target[i], getattr(node, attr)) for i, attr in enumerate(attrs)]

if __name__ == "__main__":
    unittest.main()

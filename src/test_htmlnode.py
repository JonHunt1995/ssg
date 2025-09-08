import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_props_to_html(self):
		target = ' href="https://www.google.com" target="_blank"'
		node = HTMLNode('a', "this is a link", None, {
			"href": "https://www.google.com",
			"target": "_blank",
		})
		actual = node.props_to_html()
		self.assertEqual(target, actual)

	def test_props_to_html_sorted(self):
		node = HTMLNode("a", "x", None, {"target": "_blank", "href": "https://x.com"})
		self.assertEqual(node.props_to_html(), ' href="https://x.com" target="_blank"')

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

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_a(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		target = '<a href="https://www.google.com">Click me!</a>'
		self.assertEqual(node.to_html(), target)

	def test_leaf_to_html_raises_on_none_value(self):
		node = LeafNode("p", None)
		with self.assertRaises(ValueError):
			node.to_html()

	def test_leaf_to_html_allows_empty_string(self):
		node = LeafNode("p", "")
		self.assertEqual(node.to_html(), "<p></p>")

	def test_leaf_to_html_tag_none_returns_raw_value(self):
		node = LeafNode(None, "Just text")
		self.assertEqual(node.to_html(), "Just text")

	def test_leaf_to_html_sorts_props(self):
		node = LeafNode("a", "Click", {"target": "_blank", "href": "https://x.com"})
		self.assertEqual(node.to_html(), '<a href="https://x.com" target="_blank">Click</a>')

	def test_leaf_to_html_single_prop(self):
		node = LeafNode("img", "", {"alt": "logo"})
		self.assertEqual(node.to_html(), '<img alt="logo"></img>')

	def test_leaf_has_no_children(self):
		node = LeafNode("p", "hi")
		self.assertIsNone(node.children)

	def test_leaf_ignores_children_arg(self):
		node = LeafNode("p", "hi", props={"x": 1})
		self.assertIsNone(node.children)
			
	def test_leaf_to_html_no_props(self):
		node = LeafNode("p", "x", {})
		self.assertEqual(node.to_html(), "<p>x</p>")

	def test_leaf_props_sorted_in_output(self):
		node = LeafNode("a", "Click", {"target": "_blank", "href": "https://x.com"})
		self.assertEqual(node.to_html(), '<a href="https://x.com" target="_blank">Click</a>')

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

	def test_to_html_with_single_leaf_node(self):
		child_node = LeafNode("p", "Here is some text")
		parent_node = ParentNode("div", [child_node], {"class": "container", "id": "cool"})
		self.assertEqual(
			parent_node.to_html(),
			'<div class="container" id="cool"><p>Here is some text</p></div>'
		)
		
	def test_to_html_with_multiple_leaf_nodes(self):
		children = [
			LeafNode("p", "Here is some text"),
			LeafNode("p", "Here is some text"),
			LeafNode("p", "Here is some text"),
			LeafNode("p", "Here is some text"),
		]
		parent_node = ParentNode("div", children, {"class": "container", "id": "cool"})
		self.assertEqual(
			parent_node.to_html(),
			'<div class="container" id="cool"><p>Here is some text</p><p>Here is some text</p><p>Here is some text</p><p>Here is some text</p></div>'
		)

	def test_parent_with_grandchildren(self):
		inner = ParentNode("span", [LeafNode("b", "X")])
		outer = ParentNode("div", [inner])
		self.assertEqual(outer.to_html(), "<div><span><b>X</b></span></div>")

	def test_parent_with_multiple_children(self):
		children = [
			LeafNode("p", "A"),
			LeafNode(None, "B"),
			LeafNode("i", "C"),
			LeafNode(None, "D"),
		]
		parent = ParentNode("div", children)
		self.assertEqual(parent.to_html(), "<div><p>A</p>B<i>C</i>D</div>")

	def test_parent_raises_without_tag(self):
		with self.assertRaisesRegex(ValueError, "requires a tag"):
			ParentNode(None, [LeafNode("p", "x")]).to_html()

	def test_parent_raises_with_children_none(self):
		with self.assertRaisesRegex(ValueError, "Missing children argument"):
			ParentNode("div", None).to_html()

	def test_parent_raises_with_children_empty(self):
		with self.assertRaisesRegex(ValueError, "At least one child is required"):
			ParentNode("div", []).to_html()

	def test_parent_props_rendered(self):
		parent = ParentNode("section", [LeafNode(None, "hi")], {"data-x": "1"})
		self.assertEqual(parent.to_html(), '<section data-x="1">hi</section>')
		
if __name__ == "__main__":
    unittest.main()

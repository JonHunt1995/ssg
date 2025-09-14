from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
	if not isinstance(text_node.text_type, TextType):
		raise Exception("Invalid text type")	
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"alt": text_node.text, "src": text_node.url})
		case _:
			raise Exception("Invalid text type")
		
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
	new_nodes: list[TextNode] = []
	for node in old_nodes:
		# If node type isn't text, just add to new_nodes
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
			continue
		# Break up text nodes by delim to extract nodes of target type
		new_nodes.extend(split_text_node(node, delimiter, text_type))
	return new_nodes

def split_text_node(node: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
	node_text = node.text
	output: list[TextNode] = []
	# Handles when no delims, so no need to split
	if delimiter not in node_text:
		return [node]
	# Handles when there's no matching delim
	if node_text.count(delimiter) % 2 != 0:
		raise Exception("invalid markdown syntax")
	idx = node_text.index(delimiter)
	# Used to handle when delim is at beginning
	if idx != 0:
		output.append(TextNode(node_text[:idx], TextType.TEXT))
	node_text = node_text[idx+len(delimiter):]
	try:
		idx = node_text.index(delimiter)
	except ValueError as e:
		raise Exception("invalid markdown syntax")
	if node_text[:idx]:
		output.append(TextNode(node_text[:idx], text_type))
	if idx < len(node_text):
		output.extend(split_text_node(TextNode(node_text[idx+len(delimiter):], TextType.TEXT), delimiter, text_type))
	return output
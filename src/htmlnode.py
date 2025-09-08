class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError("to_html method not implemented")
	
	def props_to_html(self):
		if self.props is None:
			return ""
		return ' ' + ' '.join([prop + '="' + val + '"' for prop, val in sorted(self.props.items(), key=lambda x: x[0])])
	
	def __repr__(self):
		attrs = ['tag', 'value', 'children', 'props']
		return self.__class__.__name__ + '(' + ', '.join([f"{attr}={getattr(self, attr)}" for attr in attrs]) + ')'
	
class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value is None:
			raise ValueError("All leaf nodes require a value")
		if not self.tag:
			return f"{self.value}"
		return f"<{self.tag}{'' if not self.props else super().props_to_html()}>{self.value}</{self.tag}>"
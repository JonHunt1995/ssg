from textnode import TextNode, TextType

def main():
	node = TextNode("this is some anchor text", TextType.LINK, "https://www.boot.dev)")
	print(node)

# python
if __name__ == "__main__":
    main()
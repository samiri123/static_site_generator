from textnode import TextNode, TextType

def main():
    print("hello world")
    dummy_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(f"dummy_node: {dummy_node}")


if __name__ == "__main__":
    main()

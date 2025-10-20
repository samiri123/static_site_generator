from textnode import TextType, TextNode
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type: TextType):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_nodes = []
            splitted_node_text = old_node.text.split(delimiter)
            if len(splitted_node_text) % 2 == 0:
                raise Exception("Opening delimiter must be closed with same delimiter.")
            else:
                for text in splitted_node_text:
                    if text == "":
                        continue
                    if text == text.strip():
                        split_nodes.append(TextNode(text, text_type))
                    else:
                        split_nodes.append(TextNode(text, TextType.TEXT))
                new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        count = 0
        sections = []
        while count < len(images):
            sections = original_text.split(f"![{images[count][0]}]({images[count][1]})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(images[count][0], TextType.IMAGE, images[count][1]))
            original_text = sections[1]
            count += 1
        new_nodes.extend(split_nodes)
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        count = 0
        sections = []
        while count < len(links):
            sections = original_text.split(f"[{links[count][0]}]({links[count][1]})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(links[count][0], TextType.LINK, links[count][1]))
            original_text = sections[1]
            count += 1
        new_nodes.extend(split_nodes)
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

node = TextNode(
    "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
    TextType.TEXT,
)
new_nodes = split_nodes_link([node])
print(new_nodes)
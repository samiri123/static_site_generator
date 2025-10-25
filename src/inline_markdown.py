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
        if old_node.text_type != TextType.TEXT: #old nodes are of type text
            new_nodes.append(old_node)
            continue
        text = old_node.text # original text
        images = extract_markdown_images(text)
        if len(images) == 0: #no images found
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1) #split only once -> two parts
            if sections[0] != "": #first part is not empty -> add it
                new_nodes.append(TextNode(sections[0], TextType.TEXT)) 
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1])) #add the image itself
            text = sections[1] #second part becomes the new text
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT)) #add the last section 
    return new_nodes

#it's similar to above function
def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        sections = []
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text: str):
    original_text_node = TextNode(text, TextType.TEXT)
    split_bold = split_nodes_delimiter([original_text_node], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_image = split_nodes_image(split_code)
    return split_nodes_link(split_image) 

from textnode import TextType, TextNode

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
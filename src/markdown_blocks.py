from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    blocks = []
    split_md = markdown.split("\n\n")
    for block in split_md:
        block = block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks


def block_to_block_type(block: str):
    md_headings = ["#", "##", "###", "####", "#####", "######"]
    if block.split()[0] in md_headings:
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in block.split("\n"):
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_html = block_to_html_node(block)
        children.append(block_html)
    return ParentNode("div", children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE: 
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    inline_html_nodes = []
    for text_node in text_nodes:
        inline_html_nodes.append(text_node_to_html_node(text_node))
    return inline_html_nodes

def paragraph_to_html_node(block):
    lines = block.split("\n")
    row_text = " ".join(lines)
    return ParentNode("p", text_to_children(row_text))

def heading_to_html_node(block):
    count_dashes = block.split()[0].count("#")
    if count_dashes + 1 >= len(block):
        raise ValueError("Heading must contain text")
    elif 1 > count_dashes > 6:
        raise ValueError("Heading must be between 1 and 6")
    row_text = block[count_dashes+1:]
    return ParentNode(f"h{count_dashes}", text_to_children(row_text))

def code_to_html_node(block):
    if not block.startswith("```") and block.endswith("```"):
        raise ValueError("Not a code block")
    row_text = block[4:-3]
    lines = row_text.split("\n")
    row_text = "\n".join(lines)
    text_node = TextNode(row_text, TextType.CODE)
    html_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [html_node])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("not a valid quote")
        new_lines.append(line.lstrip(">").strip())
    row_text = " ".join(new_lines)
    return ParentNode("blockquote", text_to_children(row_text))

def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)
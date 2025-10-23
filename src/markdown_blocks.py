
def markdown_to_blocks(markdown: str):
    blocks = []
    split_md = markdown.split("\n\n")
    for block in split_md:
        block = block.strip()
        if block == "":
            continue
        blocks.append(block)
    return blocks
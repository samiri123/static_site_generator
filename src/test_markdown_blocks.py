import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToHTML(unittest.TestCase):
    
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.md = """
This is another paragraph with _italic_ text and `code` here  
This is the same paragraph on a new line  

# This is an H1 heading  

### This is an H3 heading  

```python
def example():
    return "code block"
```

> This is a blockquote  
> It can span multiple lines  

- This is an unordered list  
- with items  
- and more items  

1. This is an ordered list  
2. with numbered items  
3. in sequence
"""     
        self.blocks = markdown_to_blocks(self.md)
        
        
    
    def test_paragraph(self):
        paragraph = self.blocks[0]
        print(paragraph)
        result = block_to_block_type(paragraph)
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_head_1(self):
        heading_1 = self.blocks[1]
        result = block_to_block_type(heading_1)
        self.assertEqual(result, BlockType.HEADING)
        
    def test_head_3(self):
        heading_3 = self.blocks[2]
        result = block_to_block_type(heading_3)
        self.assertEqual(result, BlockType.HEADING)
    
    def test_code(self):
        code = self.blocks[3]
        result = block_to_block_type(code)
        self.assertEqual(result, BlockType.CODE)
    
    def test_quote(self):
        quote = self.blocks[4]
        result = block_to_block_type(quote)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list(self):
        unordered_list = self.blocks[5]
        result = block_to_block_type(unordered_list)
        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        ordered_list = self.blocks[6]
        result = block_to_block_type(ordered_list)
        self.assertEqual(result, BlockType.ORDERED_LIST)
        
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


if __name__ == "__main__":
    unittest.main()

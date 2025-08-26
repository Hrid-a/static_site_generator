# text (plain)
# **Bold text**
# _Italic text_
# `Code text`
# Links, in this format: [anchor text](url)
# Images, in this format: ![alt text](url)

from enum import Enum

class TextType(Enum):
    TEXT = "text"            # plain text
    BOLD = "bold"            # **bold text**
    ITALIC = "italic"        # _italic text_
    CODE = "code"            # `code text`
    LINK = "link"            # [anchor](url)
    IMAGE = "image"          # ![alt](url)


class TextNode:
    def __init__(self, text:str, text_type:TextType, url:str=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type.value == other.text_type.value and self.url == other.url


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    


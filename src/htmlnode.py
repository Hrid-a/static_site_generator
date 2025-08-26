import json


class HtmlNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    
    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        str = ''
        if self.props is None:
            return str
        
        for key, value in self.props.items():
            str += f" {key}=\"{value}\""

        return str
    

    def __repr__(self):
        return (
            f"HtmlNode(tag={self.tag}, "
            f"value={self.value}, "
            f"children={self.children}, "
            f"props={json.dumps(self.props) if self.props else self.props})"
        )

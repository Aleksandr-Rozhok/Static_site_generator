class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        str_with_props = ""

        if self.props == None:
            return str_with_props
        else:
            for prop, val in self.props.items():
                str_with_props += f"{prop}=\"{val}\" "
            
            return str_with_props.strip(" ")
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, props=props)
        self.value = value
        
        if isinstance(self.tag, dict):
            self.props = self.tag
        elif not self.value and self.tag:
            self.value = self.tag
            self.tag = None
        elif self.value and self.tag or self.value and not self.tag and self.props:
            value_keeper = self.value
            self.value = self.tag
            self.tag = value_keeper        
    
    def to_html(self):
        all_single_tags = [
            "area", "base", "br", "col", "embed",
            "hr", "img", "input", "link", "meta",
            "param", "source", "track", "wbr"
            ]
        
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        elif not self.tag:
            return self.value
        elif not self.props:
            if self.tag in all_single_tags:
                return f"<{self.tag}/>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            if self.tag in all_single_tags:
                return f"<{self.tag} {self.props_to_html()}/>"
            else:
                return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, children, tag=None, props=None):
        super().__init__(tag, props)
        self.children = children

        if not isinstance(self.children, list):
            value_keeper = self.children
            self.children = self.tag
            self.tag = value_keeper
        
    def to_html(self):
        if not self.tag:
            raise ValueError("There not a tag")
        elif not self.children:
            raise ValueError("There not a children")
        else:
            result_str = f"<{self.tag}>"

            for node in self.children:
                    result_str += node.to_html()

            return result_str + f"</{self.tag}>"
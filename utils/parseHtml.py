from html.parser import HTMLParser


class HTMLProcessor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        indent = "    " * self.depth
        attr_str = " ".join(f'{key}="{value}"' for key, value in attrs)
        tag_representation = f"{indent}<{tag}{
            ' ' + attr_str if attr_str else ''}>"
        self.result.append(tag_representation)
        self.depth += 1

    def handle_endtag(self, tag):
        self.depth -= 1
        indent = "    " * self.depth
        self.result.append(f"{indent}</{tag}>")

    def handle_data(self, data):
        text = data.strip()
        if text:
            indent = "    " * self.depth
            self.result.append(f"{indent}{text}")


def parse_html(html):
    parser = HTMLProcessor()
    parser.feed(html)
    return "\n".join(parser.result).rstrip()

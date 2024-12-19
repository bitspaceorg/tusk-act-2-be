import html2text


def parse_html(html):
    text = html2text.HTML2Text()
    text.ignore_links = True
    data = "\n".join([i for i in text.handle(html).split("\n") if i.strip()])
    return data

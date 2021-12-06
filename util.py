import lxml.html


def responseToTree(response):
    response.raw.decode_content = True
    return lxml.html.parse(response.raw)
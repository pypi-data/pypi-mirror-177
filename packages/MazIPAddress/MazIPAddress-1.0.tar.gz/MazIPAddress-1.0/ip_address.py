# Author: Mazen Mahari
# Date: 18-10-2022
# Description: Module 7A - Parsing XHTML

"'HTMLParser serves as the basis for parsing text files formatted in HTML'"
from html.parser import HTMLParser
from urllib.request import urlopen


class MyHTMLParser(HTMLParser):
    "'MyHTMLParser' is a subclass of 'HTMLParser'"

    def __init__(self):
        super().__init__()
        self.body = False
        self.ip = ''

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.body = True

    def handle_endtag(self, tag):
        if tag == "body":
            self.body = False

    def handle_data(self, data):
        if self.body:
            if "IP Address" in data:
                self.ip = data.split(": ")[1].strip()


def get_ip():
    "'get_ip' returns the IP address of the current machine."
    myparser = MyHTMLParser()
    with urlopen("http://checkip.dyndns.org") as response:
        html = str(response.read())
    myparser.feed(html)
    return myparser.ip


if __name__ == "__main__":
    print(get_ip())

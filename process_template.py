from pathlib import Path
from bs4 import BeautifulSoup

def Process(path, soup):
    print("Processing...")

    element = soup.find("main")
    if element:
        element.clear()
        element.append(BeautifulSoup("<p>New content goes here</p>", "html.parser"))

    #return
    return soup
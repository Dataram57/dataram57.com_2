import os
from pathlib import Path
from bs4 import BeautifulSoup

def GetContent(path):
    with open(path, "r", encoding="utf-8") as file:
        s = file.read()
    if s:
        return s
    return False
    

def Process(sourcePath, soup):
    print("Processing...")

    #funcs
    def TryReplaceElement(name, element, add=False):
        if element:
            path = sourcePath / name
            if path.is_file():
                content = GetContent(path)         
                if content:
                    if not add:
                        element.clear()
                    element.append(BeautifulSoup(content, "html.parser"))

    #basic ones
    TryReplaceElement("head.html", soup.find("head"), True)
    TryReplaceElement("background.html", soup.find(id="background"))
    TryReplaceElement("background_window.html", soup.find(id="background_window"))
    TryReplaceElement("header.html", soup.find("header"))
    TryReplaceElement("nav.html", soup.find("nav"))
    TryReplaceElement("main.html", soup.find("main"))
    TryReplaceElement("footer.html", soup.find("footer"))

    #return
    return soup
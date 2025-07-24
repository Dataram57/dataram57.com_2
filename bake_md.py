import os
from pathlib import Path
import markdown

################################################################

used = False

def GetArticleFileName(i):
    return ("article." + str(i) + ".md")

################################################################

def Start(path):
    global used
    
    #skip if file already exist
    if (path / "main.html").is_file():
        return
        
    #count files
    i = 0
    while (path / GetArticleFileName(i)).is_file():
        i += 1

    #count down and write markdown into main.html
    html = ""
    with open(path / "main.html", "w", encoding="utf-8") as f:
        used = True
        while i > 0:
            i -= 1
            print("Including: " + str(path / GetArticleFileName(i)))
            with open(path / GetArticleFileName(i), "r", encoding="utf-8") as f2:
                f.write("<article>")
                f.write(markdown.markdown(f2.read()))
                f.write("</article>")
        

################################################################

def End(path):
    global used
    #check if was used
    if used:
        used = False
        #delete generated file
        os.remove(path / "main.html")
import json
import importlib.util
import os
from pathlib import Path
from bs4 import BeautifulSoup
import process_template

#load config
bakePath = False
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
    bakePath = config["bakePath"]
    sourcePath = config["sourcePath"]
    templatePath = config["templatePath"]

#bad config check
if not config:
    print("Couldn't load config")
    exit()

#load main html file
def LoadTemplate():
    global soup
    with open(templatePath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
LoadTemplate()

#no index.html file check
if not soup:
    print("Couldn't find template")
    exit()

#import scripts
scripts = []
for i, path in enumerate(config["scripts"]):
    name = f"plugin_{i}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    scripts.append(module)
    print(f"Imported {name}: {module}")
    
#walk over dirs
elems = [Path(sourcePath)] + list(Path(sourcePath).iterdir())
for path in elems:
    if path.is_dir():
        #preparation
        outputPath = Path(bakePath) / path.relative_to(sourcePath)
        print(f"Preparing folder📁 {path} ---> {outputPath}")
        if not outputPath.exists():
            os.makedirs(outputPath)

        #module start
        print(f"Starting scripts✨")
        for module in scripts:
            if hasattr(module, "Start"):
                module.Start(path)

        #bake html
        print(f"Baking 👨‍🍳")
        LoadTemplate()

        #Process
        process_template.Process(path, soup)

        #save generated html
        outputPath = outputPath / "index.html"
        print(f"Writing bake✍️  {outputPath}")
        with open(outputPath, "w", encoding="utf-8") as file:
            file.write(str(soup))

        #module end
        print(f"Ending scripts🛏️")
        for module in scripts:
            if hasattr(module, "End"):
                module.End(path)



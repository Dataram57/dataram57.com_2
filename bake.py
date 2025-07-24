import json
import importlib.util
import os
from pathlib import Path

#load config
bakePath = False
with open("config.json", "r", encoding="utf-8") as file:
    config = json.load(file)
    bakePath = config["bakePath"]
    sourcePath = config["sourcePath"]

#bad config check
if not bakePath:
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
for path in Path(sourcePath).iterdir():
    if path.is_dir():
        #preparation
        outputPath = Path(bakePath) / path.relative_to(sourcePath)
        print(f"Preparing folder📁 {path} ---> {outputPath}")
        if not outputPath.exists():
            os.makedirs(outputPath)

        #module start
        for module in scripts:
            if hasattr(module, "Start"):
                module.Start(path)

        #bake html

        

        #module end
        for module in scripts:
            if hasattr(module, "End"):
                module.End(path)
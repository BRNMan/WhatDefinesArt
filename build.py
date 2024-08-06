import os
from datetime import date
import random
import shutil

dirBuildBase = "./build"
# Set up build directory
if(os.path.isdir(dirBuildBase)):
    shutil.rmtree(dirBuildBase)
os.mkdir(dirBuildBase)

# Copy files that don't need processing
otherFiles = list(filter(lambda file: file.endswith((".js",".css",".png",".jpg")), os.listdir("./")))
for file in otherFiles:
    shutil.copyfile(file, "./build/" + file)

# Process other files
myFile =  open("index.htm","r")
fileText = myFile.read()
myFile.close()
imageDirFiles = os.listdir("./images")
imageFiles = list(filter(lambda img: img.endswith(".jpg"), imageDirFiles))

random.seed(date.today().isoformat())
curImage = random.choice(imageFiles)

shutil.copyfile("./images/" + curImage, dirBuildBase + "/" + curImage)

fileText = fileText.replace("{#RandomImage#}", '"./' + curImage + '"')

f = open(dirBuildBase + "/index.html", "w")
f.write(fileText)
f.close()


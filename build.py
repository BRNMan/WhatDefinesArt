import os
from datetime import date
import random

myFile =  open("index.htm","r")
fileText = myFile.read()
myFile.close()
imageDirFiles = os.listdir("./images")
imageFiles = list(filter(lambda img: img.endswith(".jpg"), imageDirFiles))

random.seed(date.today().isoformat())
curImage = random.choice(imageFiles)

fileText = fileText.replace("{#RandomImage#}", '"./images/' + curImage + '"')

f = open("index.html", "w")
f.write(fileText)
f.close()


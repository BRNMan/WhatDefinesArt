import os
from datetime import date
import random
import shutil
import sqlite3
import datetime
import hashlib
import logging

logging.info("Rebuilding What Defines Art")

def chooseNewPicture():
    return True

dirBuildBase = "./build/"
staticSrcBase = "./static_src/"
imagesBase = "./images/"
# Set up build directory
if(os.path.isdir(dirBuildBase)):
    shutil.rmtree(dirBuildBase)
os.mkdir(dirBuildBase)
os.mkdir(dirBuildBase + "randomImage/")

# Copy files in static_src directory to build directory
otherFiles = list(os.listdir(staticSrcBase))
for file in otherFiles:
    shutil.copyfile(staticSrcBase + file, dirBuildBase + file)

# Process other files
myFile =  open(staticSrcBase + "index.htm","r")
fileText = myFile.read()
myFile.close()
imageDirFiles = os.listdir(imagesBase)
imageFiles = list(filter(lambda img: img.endswith(".jpg"), imageDirFiles))

random.seed(date.today().isoformat())
curImage = random.choice(imageFiles)
curImageMD5 = hashlib.md5(open(imagesBase + curImage,'rb').read()).hexdigest()

shutil.copyfile(imagesBase + curImage, dirBuildBase + "randomImage/" + curImage)

fileText = fileText.replace("{#RandomImage#}", "randomImage/" + curImage)

f = open(dirBuildBase + "index.html", "w")
f.write(fileText)
f.close()

with sqlite3.connect("site_data.db") as con:
    try:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS"Pictures" (
        "Filename"	TEXT,
        "Date_Displayed"	TEXT,
        "Yes_Votes"	INTEGER DEFAULT 0,
        "No_Votes"	INTEGER DEFAULT 0,
        "Picture_Hash"	TEXT,
        PRIMARY KEY("Filename","Date_Displayed")
        );""")
        cur.execute("""CREATE TABLE IF NOT EXISTS "Votes" (
        "UserID"	TEXT,
        "Choice"	TEXT,
        "Time"	TEXT,
        "Date_Displayed_FK"	TEXT,
        "Filename_FK"	TEXT,
        FOREIGN KEY("Date_Displayed_FK") REFERENCES "Pictures"("Date_Displayed"),
        FOREIGN KEY("Filename_FK") REFERENCES "Pictures"("Filename")
        )""")
        cur.execute("""INSERT OR IGNORE INTO "Pictures" (Filename,Date_Displayed,Yes_Votes,No_Votes,Picture_Hash)
        VALUES(?,?,0,0,?)""",
        (curImage, datetime.date.today().strftime('%Y-%m-%d'), curImageMD5))
        con.commit()
    except Exception as E:
        logging.exception("There was a SQL error.")
        con.rollback()


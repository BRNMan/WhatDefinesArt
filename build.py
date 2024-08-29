import os
from datetime import date
import random
import shutil
import sqlite3
import datetime
import hashlib
import logging
import drivePictures

logging.info("Rebuilding What Defines Art")

def chooseNewPicture():
    return True

dirBuildBase = "./build/"
staticSrcBase = "./static_src/"
imagesBase = "./images/"

# First make sure we're in the directory this file is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
 
# Next set up the build directory
if(os.path.isdir(dirBuildBase)):
    shutil.rmtree(dirBuildBase)
os.mkdir(dirBuildBase)
randomImageBase = dirBuildBase + "randomImage/"
os.mkdir(randomImageBase)

# Copy files in static_src directory to build directory
otherFiles = list(os.listdir(staticSrcBase))
for file in otherFiles:
    shutil.copyfile(staticSrcBase + file, dirBuildBase + file)

# Process other files
myFile =  open(staticSrcBase + "index.htm","r")
fileText = myFile.read()
myFile.close()

# Get our image from drive
curImageFileName = drivePictures.download_random_image(randomImageBase)

curImageMD5 = hashlib.md5(open(randomImageBase + curImageFileName,'rb').read()).hexdigest()

# In the html we work in the context of the build directory so no /build prefix necessary
fileText = fileText.replace("{#RandomImage#}", "randomImage/" + curImageFileName)

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
        (curImageFileName, datetime.date.today().strftime('%Y-%m-%d'), curImageMD5))
        con.commit()
    except Exception as E:
        logging.exception("There was a SQL error.")
        con.rollback()


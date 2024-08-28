from fastapi import FastAPI,HTTPException,Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
import os
import datetime

if __debug__:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

@app.get("/")
async def root():
    return FileResponse("build/index.html")

class Choice(BaseModel):
    choice: str = ""

@app.post("/vote")
async def vote(choice: Choice, request: Request):
    if not (choice.choice == "yes" or choice.choice == "no"):
        raise HTTPException(status_code=400,detail="Error: Invalid Vote")
        
    try:
        with sqlite3.connect("site_data.db") as con:
            cur = con.cursor()

            # Get host IP address
            userIP = request.client.host
            hasUserVoted = False
            # Check if user has voted today
            current_date = datetime.date.today().strftime('%Y-%m-%d')
            res = cur.execute("SELECT Choice FROM 'Votes' WHERE UserID=? AND Date_Displayed_FK=?",(userIP,current_date))
            # If the user has already voted today, stop them
            if(res.fetchone() is not None):
                hasUserVoted = True

            # Check how many votes the picture has
            filename = list(os.listdir("./build/randomImage/"))[0]
            print(filename)
            res = cur.execute("SELECT Yes_Votes, No_Votes FROM Pictures WHERE Filename=? AND Date_Displayed=?", (filename,current_date))
            [yes_votes,no_votes] = res.fetchone()

            if hasUserVoted:
                msg = str(yes_votes) + "," + str(no_votes)
                return msg

            if(choice.choice == "yes"):
                yes_votes += 1
            elif(choice.choice == "no"):
                no_votes += 1

            msg = str(yes_votes) + "," + str(no_votes)
            # Create a new vote
            cur.execute("""INSERT INTO 'Votes' (UserID, Choice, Time, Filename_FK, Date_Displayed_FK) 
                        VALUES(?,?,?,?,?)""", 
                        (userIP, choice.choice, datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S'), filename, current_date))

            # Update the picture's votes
            cur.execute("""UPDATE 'Pictures' 
                        SET Yes_Votes=?,
                            No_Votes=?
                        WHERE Filename=? AND Date_Displayed=?""",
                        (yes_votes, no_votes, filename, current_date))
            
            con.commit()

            print("Voted: " + choice.choice)
            return msg
    except Exception as E:
        con.rollback()
        if type(E) == HTTPException:
            raise E
        raise HTTPException(status_code=400,detail="Error: Invalid Vote")
        

# Do this afterwards the get root mount
app.mount("/", StaticFiles(directory="build"), name="static")
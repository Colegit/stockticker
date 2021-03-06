print("calling to flask")
from flask import Flask, request, json, jsonify
import sqlite3
from datetime import datetime


app = Flask(__name__)

@app.route('/insert', methods=['POST'])
def dbconnect():

  frontdata = json.loads(request.data)
  print(frontdata)
  print(frontdata.get('content'))
  #json extraction of individual values from a 2d json https://stackoverflow.com/questions/47729562/how-to-address-multidimensional-json-array-in-python/47729655
  print(frontdata['content']['pain'])

  # Variables of the values from the passed in from the json sent from the frontend
  pain        = frontdata['content']['pain']
  excersise   = frontdata['content']['excersise']
  setback     = frontdata['content']['setback']
  setbackdesc = frontdata['content']['setbackdesc']
  doc         = frontdata['content']['doc']
  
  notes       = frontdata['content']['notes']
  curtime     = datetime.now()
  day         = curtime.date()
  time        = curtime.strftime("%H:%M")

  #If no data is entered for doctor description and py tries to access the 'title' of the doctor, it will return an error as no doctor title was entered. 
  try:
    docdesc   = frontdata['content']['docdesc']['title']
  except:
    docdesc   = ""

  print(docdesc)

  print(day)
  print(time)

  print(setbackdesc)

  print(notes)

  params = (pain, excersise, setback, setbackdesc, doc, docdesc, notes, day, time)


  

  db = sqlite3.connect('../injurydb.db')
  cursor = db.cursor()
  cursor.execute("INSERT INTO dataentry (pain, excersise, setback, setbackdesc, docvisit, doctype, notes, todaydate, currenttime) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", params)
  db.commit()


  return 'dbconnect'

@app.route('/averagepain', methods=['GET'])
def avgpain():
  db = sqlite3.connect('../injurydb.db')
  cursor = db.cursor()
  cursor.execute("Select pain, todaydate, setbackdesc from dataentry")
  
  results = cursor.fetchall()
  print(results)
  return jsonify(results)


if __name__=='__main__':
  app.run(port=5000, debug=True)

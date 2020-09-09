from flask import Flask, render_template, request, redirect, url_for
import pymongo
from pymongo import MongoClient
from randomstr import randomstr
import os

password = os.getenv('password')
  
client = pymongo.MongoClient(f"mongodb+srv://dbUser:{password}@cluster0-guvcd.mongodb.net/test?retryWrites=true&w=majority", 27107)

db = client['main-db']

collection = db['main-collection']

app = Flask(__name__, static_url_path='/static')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('err3.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('err2.html'), 500

@app.route('/err1')
def e1():
  return render_template('err1.html')

@app.route('/', methods=['POST', 'GET'])
def main():
    return render_template('input.html')

@app.route('/makePaste', methods=['POST', 'GET'])
def mp():
  if request.method=='POST':
    contents = request.values.get('content')
    if len(contents) > 50000:
      return redirect('/err1', 302)
    else:
      x = randomstr(length=10, charset='alphanumeric', readable=False, capitalization=False)
      print("Contents:", contents)
      print("ID:", x)
      collection.insert_one({
        'content': contents,
        'binid': x
      })
      return redirect(f'/bins/{x}', 302)
  else:
    return redirect('/', 302)

@app.route('/bins/<binid>')
def bins(binid):
  contents = str(collection.find_one({'binid': binid})['content'])
  return render_template('bin.html', binid=binid, contents=contents)

@app.route('/search', methods=["GET", "POST"])
def search():
  if request.method == 'GET':
    return render_template('search.html')
  if request.method == 'POST':
    data = request.form
    user = data['searchquery']
    print (user)
    return redirect(f'/bins/{user}', 302)

app.run(host='0.0.0.0',port=8080)
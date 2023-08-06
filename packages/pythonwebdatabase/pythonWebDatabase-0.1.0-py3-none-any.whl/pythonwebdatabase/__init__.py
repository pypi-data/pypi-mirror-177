__version__ = '0.1.0'

import requests
from bs4 import BeautifulSoup
import json
import html

def getBodyContents(site):
  page = requests.get(site).content
  soup = BeautifulSoup(page)
  body = soup.find('body')
  #return body.findChildren(recursive=False)
  return body
def create(db, password):
  contents = getBodyContents("https://php-database.intelligent-hacker.repl.co/?operation=create&db="+db+"&password="+password)
  return contents
class DB:
  def __init__(self, db, password):
    self.db = db
    self.password = password
    
  def set(self, key, val):
    contents = getBodyContents("https://php-database.intelligent-hacker.repl.co/?operation=set&db="+self.db+"&password="+self.password+"&key="+key+"&value="+val)
    return contents
  def read(self, key):
    contents = getBodyContents("https://php-database.intelligent-hacker.repl.co/?operation=getKey&db="+self.db+"&password="+self.password+"&key="+key)
    try:
      val = html.unescape(str(contents)[7:][:-7].strip())
      val = val.replace("%20", " ")
      return json.loads(val)
    except:
      val = html.unescape(str(contents)[7:][:-7].strip())
      val = val.replace("%20", " ")
      return val
  def readAll(self):
    contents = getBodyContents("https://php-database.intelligent-hacker.repl.co/?operation=getAll&db="+self.db+"&password="+self.password+"")
    val = html.unescape(str(contents)[7:][:-7].strip())
    val = val.replace("%20", " ")
    return json.loads(val) 
  def delete(self, key):  
    contents = getBodyContents("https://php-database.intelligent-hacker.repl.co/?operation=delete&db="+self.db+"&password="+self.password+"&key="+key)
    return contents
  def destroy(self):  
    contents = getBodyContents("https://php-database.intelligent-hacker.repl.co/?operation=destroy&db="+self.db+"&password="+self.password+"")
    return contents
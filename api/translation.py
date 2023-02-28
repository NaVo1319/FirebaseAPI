from http.server import HTTPServer
import pyrebase
from http.server import BaseHTTPRequestHandler
import json
import requests
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.wfile.write("Service is work".encode())
        return
    def do_POST(self):
        content_len = self.rfile.read(int(self.headers.get('Content-Length')))
        content = json.loads(content_len)
        firebase = pyrebase.initialize_app(config)
        database = firebase.database()
        transData = {
              "text":content["message"],
              "to":content["toLang"],
              "from":content["fromLang"]
          }
        print(transData)
        res = requests.post("https://translation-service-iota.vercel.app/api/index.py",json = transData)
        if(res.status_code == 200):
          print(res.text)
          data = {"message": res.text.encode('latin1').decode('utf8'), "target": content["target"], "sender": content["sender"]}
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.end_headers()
          database.child("messages").child(content["target"]).child().push(data)
          self.wfile.write("ok".encode())
        self.send_response(res.status_code)

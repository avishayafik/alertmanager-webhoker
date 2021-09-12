import time

import requests


class argo_events():
    def __init__(self,url,data):
        self.data = data
        self.url = url
        #self.token = token
        #self.username = username
        #self.password = password
    def argo_run(self):
          timestamp = time.strftime("%Y-%m-%d %X")
          response = requests.post(self.url ,data=self.data, headers={"content-type": "application/json"},timeout=3)
          #response = requests.post(self.url, auth=(self.username, self.password),data=self.data, headers={"content-type": "application/json"},timeout=3)
          print  (timestamp + ': running http hook , see the below response :')
          print  (response.content)
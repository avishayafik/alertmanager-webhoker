from flask import Flask
app = Flask(__name__)
from flask import Flask
from flask import request
app = Flask(__name__)
import requests
from jenkins_class import Jenkins_class
from argo_events import argo_events
import yaml
import os
from email_notification import email
from flask import Flask, render_template
#from uptime import uptime
import time
from prometheus_flask_exporter import PrometheusMetrics
from select_mysql import Mysql_query_class
import logging, sys
app = Flask(__name__)
metrics = PrometheusMetrics(app)
import json


startTime = time.time()

JSON_DISPLAY = ""
JSON_DISPLAY_LIST = []

logger = logging.getLogger('webhooker' + ' ')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.__stdout__)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(lineno)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


data = yaml.load(open('config.yaml'))
print ("alert config:")
print(data['limit'])

jenkins_token = (os.environ['jenkins_token'])
username = (os.environ['awx_username'])
password = (os.environ['awx_password'])
smtp_username = (os.environ['smtp_username'])
smtp_password = (os.environ['smtp_password'])
mysql_password = (os.environ['mysql_password'])
mysql_host = (data['mysql_host'])


class awx():
    def __init__(self,url,data,username,password):
        self.data = data
        self.url = url
        self.username = username
        self.password = password
    def awx(self):
          timestamp = time.strftime("%Y-%m-%d %X")
          response = requests.post(self.url, auth=(self.username, self.password),data=self.data, headers={"content-type": "application/json"},timeout=3)
          print  (timestamp + ': running http hook , see the below response :')
          print  (response.content)

class flask_monitor():
    def __init__(self,path):
        self.path = path



    def run_prom(self):
          response = requests.get('http://127.0.0.1:5000/alerts/' + self.path)
          print  ('send http request to /alerts :')
          print(response.content)



@app.route('/postjson', methods=['POST'])
def post():
    timestamp = time.strftime("%Y-%m-%d %X")
    app.logger.info('Info')
    logger.info('request json: '+  str(request.is_json))
    content = request.get_json()
    global JSON_DISPLAY_LIST
    global JSON_DISPLAY
    JSON = request.get_json()
    JSON_DISPLAY = JSON
    JSON_DISPLAY = json.dumps(JSON_DISPLAY)
    JSON_DISPLAY_LIST.append(JSON_DISPLAY)
    #JSON_DISPLAY = JSON_DISPLAY.replace("'", '"')
    alerts_list  = content['alerts']
    status = content['alerts'][0]['status']
    content = (content['commonLabels']['alertname'])
    #logger.info('alertname:', content)
    try:
       instance = (JSON['commonLabels']['instance'])
       #print(instance)
    except Exception:
       pass
    ### add flink app support
    try:
       flink_app = (JSON['commonLabels']['metric_name'])
       dc = (JSON['commonLabels']['site'])
       collection = (JSON['commonLabels']['collection'])
    except Exception:
       pass
    print_action = False
    blocked_alert = False
    for key in data['limit'].items():
        if content in (key[1]['alertname']) and status == (key[1]['status']):
               json_to_send = key[1]['alertname'][content]
               try:
                   ##### support in multi instnace limit
                   instance_list = []
                   for i in alerts_list:
                       instance = i['labels']['instance']
                       instance = instance = instance.split(':')
                       instance = instance[0]
                       # print(instance)
                       instance_list.append(instance)
                   instance_list = str(instance_list)
                   instance_list = instance_list.replace("[", "")
                   instance_list = instance_list.replace("'", "")
                   instance_list = instance_list.replace("]", "")
                   #instance = instance.split(':')
                   #instance =  instance[0]
                   json_to_send = json_to_send.replace('INSTANCE',instance_list)
                   logger.info(timestamp + ': vars were replaced to '+ json_to_send)
               except Exception:
                   pass
               try:
                   json_to_send = json_to_send.replace('FLINK_APP', flink_app)
                   json_to_send = json_to_send.replace('DC', dc)
                   json_to_send = json_to_send.replace('COLLECTION', collection)
               except Exception:
                   pass
               ### check in mysql if it is blocked
               try:
                   query = "select  * from alert WHERE time > DATE_SUB(NOW(), INTERVAL '%s' MINUTE)  and name='%s' and vars='%s';" % ((key[1]['blocked']),content,json_to_send)
                   Mysql_query_obj = Mysql_query_class(query, alert, mysql_password,mysql_host)
                   blocked_alert = Mysql_query_obj.mysql_query()
               except Exception:
                   pass
               if blocked_alert == False:
                   logger.info(timestamp + ': send http webhook to:')
                   logger.info(timestamp + ': ' + (key[1]['url']))
                   logger.info(timestamp + ': vars sent:' + json_to_send )
                   #### send  alert awx, argo or jenkins
                   if key[1]['type'] == 'argo_workflow':
                        argo = argo_events((key[1]['url']),json_to_send,username,password)
                        argo.argo_run()
                   elif key[1]['type'] == 'jenkins':
                       run_jenkins = Jenkins_class((key[1]['url']),json_to_send,jenkins_token,key[1]['alertname']['job'])
                       run_jenkins.build_job()
                   else:
                       runawx = awx((key[1]['url']), json_to_send, username, password)
                       runawx.awx()

                   ### send email
                   logger.info('sending email to: '+ key[1]['email'] )
                   try:
                       if key[1]['status'] == 'resolved':
                           color = 'green'
                       else:
                           color = 'red'
                       email_meassge = key[1]['email_message']
                       subject = key[1]['email_message']
                       Email = email(fromaddr="no-noreply@startapp.com", toaddr=key[1]['email'],smtp=data['smtp'], smtp_port=data['smtp_port'],
                                     subject=subject, email_message=email_meassge, username=smtp_username, password=smtp_password)
                       Email.send_email_html(color)
                   except Exception:
                       pass
                       email_meassge = ""
                       subject = content + ' alert was running awx job'
                       Email = email(fromaddr="no-noreply@startapp.com", toaddr=key[1]['email'],smtp=data['smtp'], smtp_port=data['smtp_port'],
                                     subject=subject, email_message=email_meassge, username=smtp_username, password=smtp_password)
                       Email.send_email()
                   print_action = True
                   ### send http request to register it prometheus exporter
                   run_flask_monitor = flask_monitor(content)
                   run_flask_monitor.run_prom()
                   if print_action :
                       logger.info(timestamp + ': task was running for  ' + content)
                       ### insert into mysql so it will be blocked next time
                       query = "INSERT INTO alert (name,vars) values ('%s','%s');" % (content,json_to_send)
                       Mysql_query_obj = Mysql_query_class(query, alert, mysql_password,mysql_host)
                       blocked_alert = Mysql_query_obj.mysql_insert()
                   else:
                       logger.info (timestamp + ': Nothing to do')
                   logger.info(content)
               else:
                   logger.warning(content + " : is blocked for '%s' minutes , see config.yaml" %str((key[1]['blocked'])))
    return content

@app.route("/")

def home():
    run_result_obj = Mysql_query_class(query, alert, mysql_password,mysql_host)
    run_results = run_result_obj.mysql_get_results()
    global  JSON_DISPLAY_LIST
    JSON_DISPLAY_LIST =  JSON_DISPLAY_LIST[-20:]
    return render_template("home.html",rules=data['limit'],uptime=time.time() - startTime,run_results=run_results,json_results=JSON_DISPLAY_LIST)

## making sure there is alert table
query = "CREATE TABLE IF NOT EXISTS mysql.alert ( name  VARCHAR(255), vars VARCHAR(255), time TIMESTAMP );"
alert = 'test'
Mysql_query_obj = Mysql_query_class(query, alert, mysql_password,mysql_host)
Mysql_query_obj.mysql_drop_create_table()

#run_results = Mysql_query_obj.mysql_get_results()


## running flask webservice
app.run(host='0.0.0.0', port=5000)

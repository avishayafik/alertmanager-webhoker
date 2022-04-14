import jenkins


# It comes with pip module python-jenkins
# use pip to install python-jenkins

# Jenkins Authentication URL



class Jenkins_class():
    def __init__(self ,JENKINS_URL,JENKINS_USERNAME,JENKINS_TOKEN,JOB):
        self.JENKINS_URL = JENKINS_URL
        self.JENKINS_USERNAME = JENKINS_USERNAME
        self.JENKINS_TOKEN = JENKINS_TOKEN
        self.JENKINS_JOB = JOB
        self.jenkins_server = jenkins.Jenkins(self.JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_TOKEN)
        user = self.jenkins_server.get_whoami()
        version = self.jenkins_server.get_version()
        #print ("Jenkins Version: {}".format(version))
        print ("Jenkins User: {}".format(user['id']))

    def build_job(self):
        next_build_number = self.jenkins_server.get_job_info(self.JENKINS_JOB)['nextBuildNumber']
        self.jenkins_server.build_job(self.JENKINS_JOB, token=self.JENKINS_TOKEN)
        print("build number is" ,next_build_number)
        #time.sleep(10)
        #build_info = self.jenkins_server.get_build_info(self.JENKINS_JOB, next_build_number)
        #return build_info

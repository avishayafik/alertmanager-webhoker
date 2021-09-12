# importing required library
import mysql.connector


class Mysql_query_class():
    def __init__(self,query,alert,password):
        self.query = query
        self.password = password
        self.alert = alert
        self.dataBase = mysql.connector.connect(
            host="ds-2.hosts-app.com",
            user="root",
            passwd=password,
            database="mysql")
        self.cursorObject = self.dataBase.cursor()

    def mysql_get_results(self):
        query = "select  * from alert order by time desc limit 2000"
        self.cursorObject.execute(query)
        # disconnecting from server
        myresult = self.cursorObject.fetchall()
        #print(myresult)
        self.dataBase.close()
        return myresult

    def mysql_query(self):
        query = self.query
        self.cursorObject.execute(query)
        # disconnecting from server
        myresult = self.cursorObject.fetchall()
        print(myresult)
        self.dataBase.close()
        if myresult:
            return True
        else:
            return False

    def mysql_insert(self):
        query = self.query
        self.cursorObject.execute(query)
        # disconnecting from server
        print('insert alert into mysql: ' +  query)
        self.dataBase.commit()
        self.dataBase.close()

    def mysql_drop_create_table(self):
        #self.query = "CREATE TABLE IF NOT EXISTS mysql.alert ( name  VARCHAR(255), time TIMESTAMP );"
        query = self.query
        self.cursorObject.execute(query)
        # disconnecting from server
        #self.dataBase.commit()
        self.dataBase.close()




#query = "select  * from alert ;"

#password = "test"

#alert = 'test'

#Mysql_query_obj = Mysql_query_class(query,alert,password)
#test = Mysql_query_obj.mysql_get_results()

#print(test)

#for i in test:
#    print(i)


### insert
#query = "INSERT INTO alert (name) values ('test');"
#password = "test"
#alert = 'test'
#Mysql_query_obj = Mysql_query_class(query,alert,password)
#Mysql_query_obj.mysql_insert()
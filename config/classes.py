import psycopg2
from reports.models import Report, ReportHistory
from config.models import Connection, Credential
from config.encryption import decrypt_message
from ldap3 import Server, Connection as Conn, ALL, NTLM
from django.utils import timezone
from datetime import timedelta
from pymysqlpool import  pool
from django.conf import settings
import cx_Oracle,json,pymysql
import requests
from django.utils.timezone import now

class APIConnector:
    POST='POST'
    GET='GET'
    PATCH='PATCH'
    PUT='PUT'
    def __init__(self,connection):
        self.request = None
        self.connection = connection
        pass
    def call_api(self,url_path='/', method='GET', headers={}, data={}, verify=False, proxies={},params={},json={}):
        print(f"Calling: {self.connection.host}{url_path}")
        if method=='GET':
            self.request = requests.get(f"{self.connection.host}{url_path}", data=data, headers=headers, verify=verify, proxies=proxies,params=params,json=json)
        elif method=='POST':
            self.request = requests.post(f"{self.connection.host}{url_path}", data=data, headers=headers, verify=verify,proxies=proxies,params=params,json=json)
        elif method=='PATCH':
            self.request = requests.patch(f"{self.connection.host}{url_path}", data=data, headers=headers, verify=verify,proxies=proxies,params=params,json=json)
        elif method=='PUT':
            self.request = requests.put(f"{self.connection.host}{url_path}", data=data, headers=headers, verify=verify,proxies=proxies,params=params,json=json)
        else:
            raise NotImplementedError("Unrecognized HTTP Method")

#Putting this here for Roy, he would appreciate it
class DatabaseConnector:
    def __init__(self, conn_obj):
        self.conn_obj= conn_obj

    def test_connection(self):
        raise NotImplementedError
    def commit(self):
        raise NotImplementedError
    def open_connection(self):
        raise NotImplementedError
    def close_connection(self):
        raise NotImplementedError
    def run_report(self, report):
        report_attributes = json.loads(report.attributes)
        result = self.execute_query(report.code, **report_attributes)
        history = ReportHistory()
        history.report = report
        history.data = json.dumps(result)
        history.creation_date = timezone.now()
        history.save()
    def execute_query(self, query,**kwargs):
        raise NotImplementedError
    def execute_update(self, query,auto_commit=True,**kwargs):
        raise NotImplementedError


class OracleConnector(DatabaseConnector):

    def __init__(self, conn_obj):
        super().__init__(conn_obj)

    def commit(self):
        self.connection.commit()
    def test_connection(self):

        if 'service' in json.loads(self.conn_obj.attributes):
            conn = cx_Oracle.connect(self.conn_obj.credential.username,
                                              decrypt_message(self.conn_obj.credential.password),
                                              cx_Oracle.makedsn(self.conn_obj.host, self.conn_obj.port,
                                                                service_name=json.loads(self.conn_obj.attributes)[
                                                                    'service']))
        else:

            # handle sid case
            conn = cx_Oracle.connect(self.conn_obj.credential.username,
                                              decrypt_message(self.conn_obj.credential.password),
                                              cx_Oracle.makedsn(self.conn_obj.host, self.conn_obj.port,
                                                                sid=json.loads(self.conn_obj.attributes)[
                                                                    'sid']))
        print(f"Created new connection to:{self.conn_obj.host} ")
        conn.close()
        print(f"Closed connection to:{self.conn_obj.host}")
    def open_connection(self):
        # print(settings.DATABASE_POOL)
        #basically change this to check for existing connection in settings, if so use it, otherwise create it
            #put a new connection in the pool and set the timeout to an hour from now
        try:
            self.connection = self.pool.acquire()
            print(f"Loaded existing connection to:{self.conn_obj.host} ")
        except:
            print(json.loads(self.conn_obj.attributes))
            if 'service' in json.loads(self.conn_obj.attributes):
                self.pool = cx_Oracle.SessionPool(self.conn_obj.credential.username, decrypt_message(self.conn_obj.credential.password),
                                  cx_Oracle.makedsn(self.conn_obj.host, self.conn_obj.port,
                                                    service_name=json.loads(self.conn_obj.attributes)['service']))
            else:

                #handle sid case
                self.pool = cx_Oracle.SessionPool(self.conn_obj.credential.username,
                                                  decrypt_message(self.conn_obj.credential.password),
                                                  cx_Oracle.makedsn(self.conn_obj.host, self.conn_obj.port,
                                                                    sid=json.loads(self.conn_obj.attributes)[
                                                                        'sid']))
            self.connection = self.pool.acquire()
            print(f"Created new connection to:{self.conn_obj.host} ")

    def run_report(self, report):
        super().run_report(report)

    def execute_function(self, _function,return_type, args_list):
        try:
            cursor = self.connection.cursor()
            result =  cursor.callfunc(_function, return_type, args_list)
            cursor.close()
            return result
        except Exception as e:
            print(f'{str(e)}')
            # result.append()
            cursor.close()
            raise e

    def execute_query(self, query, **kwargs):
        result=[]

        cursor = self.connection.cursor()
        try:
            if 'verbose' in kwargs:
                if kwargs['verbose']:
                    print(query)
            # print("cursor opened")
            cursor.execute(query)
            # print("query executed")
            result.append([row[0] for row in cursor.description])
            for row in cursor.fetchall():
                result.append([str(x) for x in row])

            cursor.close()
            # print("cursor closed")
        except Exception as e:
            print(f'{str(e)}')
            # result.append()
            cursor.close()
            raise e
        return result
    def execute_update(self, query, auto_commit=True,**kwargs):
        # result = []

        cursor = self.connection.cursor()
        try:
            # print("cursor opened")
            print(query)
            cursor.execute(query)
            if auto_commit:
                self.connection.commit()
            # print("query executed")

            # result.append([row[0] for row in cursor.description])
            # for row in cursor.fetchall():
            #     result.append([str(x) for x in row])
            rowcount = cursor.rowcount
            cursor.close()
            return rowcount
            # print("cursor closed")
        except Exception as e:
            print(f'{str(e)}')
            # result.append()
            cursor.close()
            raise e


        # return result
    def close_connection(self):
        try:
            self.pool.release(self.connection)
            print(f"Released connection to:{self.conn_obj.host}")
        except:
            try:
                print(f"Connection: {self.conn_obj.name} could not be released, closing pool")
                self.pool.close()  # this should close the reference to the DB globally
            except:
                print(f"{self.conn_obj.name} has a pool that is already inactive")
            print(f"Closed connection to:{self.conn_obj.host}")



class LDAPConnector(DatabaseConnector):
    def __init__(self, conn_obj):
        super().__init__(conn_obj)

    def commit(self):
        self.conn.commit()
    def open_connection(self):
        server = Server(self.conn_obj.host, port=int(self.conn_obj.port), get_info=ALL)
        ldap_conn = Conn(server, user=self.conn_obj.credential.username, password=decrypt_message(self.conn_obj.credential.password))

        self.conn = ldap_conn
        if not self.conn.bind():
            print(f"error in bind {self.conn.result}")
            raise  Exception(f"error in bind {self.conn.result}")

    def close_connection(self):
        try:
            if not self.conn.unbind():
                print(f"error in bind {self.conn.result}")
                raise Exception(f"error in bind {self.conn.result}")
        except Exception as e:
            raise e
    def execute_query(self, query,**kwargs):
        if 'dn' not in kwargs:
            raise Exception("no DN provided")
        print(f"searching dn {kwargs['dn']} for {query}")
        self.conn.search(kwargs['dn'], query, attributes=['*'])
        attributes = []
        results = []
        for entry in self.conn.response:
            results.append([entry['dn'], entry['attributes']])
            for key in entry['attributes'].keys():
                if key not in attributes:
                    attributes.append(key)

        # form our header now
        full_data = [['dn']]
        for attribute in attributes:
            full_data[0].append(attribute)

        for entry in results:
            row = []
            row.append(entry[0])
            for i in range(1, len(full_data[0])):
                if full_data[0][i] in entry[1]:
                    if type(entry[1][full_data[0][i]]) == str:

                        row.append(entry[1][full_data[0][i]])
                    elif type(entry[1][full_data[0][i]]) == list:
                        row.append(','.join([ str(x) for x in entry[1][full_data[0][i]]]))
                    else:
                        row.append("")
                else:
                    row.append("")

            full_data.append(row)
        return full_data
    def execute_update(self, query,auto_commit=True,**kwargs):
        self.conn.modify(kwargs['dn'], {kwargs['attribute']: [(kwargs['operation'], [kwargs['value']])]})
    def test_connection(self):
        server = Server(self.conn_obj.host, port=int(self.conn_obj.port),get_info=ALL)
        ldap_conn = Conn(server, user=self.conn_obj.credential.username,
                         password=decrypt_message(self.conn_obj.credential.password))
        self.conn = ldap_conn
        if not self.conn.bind():
            print(f"error in bind {self.conn.result}")
            raise  Exception(f"error in bind {self.conn.result}")
        print(f"connected to LDAP")
        if not self.conn.unbind():
            print(f"error in bind {self.conn.result}")
            raise Exception(f"error in bind {self.conn.result}")

        print(f"disconnected LDAP")
    def run_report(self, report):
        super().run_report(report)

class MySQLConnector(DatabaseConnector):
    def __init__(self, conn_obj):
        self.conn_obj= conn_obj

    def commit(self):
        pass
    def open_connection(self):


        try:
            self.connection = self.pool.get_conn()
            print(f"Loaded existing connection to:{self.conn_obj.host} ")
        except:
            self.pool = pool.Pool(host=self.conn_obj.host, user=self.conn_obj.credential.username, passwd=decrypt_message(self.conn_obj.credential.password), port=int(self.conn_obj.port), db=json.loads(self.conn_obj.attributes)['schema'])
            self.pool.init()
            self.connection = self.pool.get_conn()
            print(f"Created new connection to:{self.conn_obj.host} ")



    def run_report(self, report):
        super().run_report(report)


    def execute_query(self, query,**kwargs):
        result=[]
        try:
            cursor = self.connection.cursor()
            # print("cursor opened")
            cursor.execute(query)
            # print("query executed")
            result.append([row[0] for row in cursor.description])
            for row in cursor.fetchall():
                result.append([str(x) for x in row])

            cursor.close()
            # print("cursor closed")
        except Exception as e:
            print(f'{str(e)}')
            # result.append()
            cursor.close()
        return result
    def execute_update(self, query,auto_commit=True,**kwargs):
        # result = []

        try:
            cursor = self.connection.cursor()
            # print("cursor opened")

            cursor.execute(query)
            cursor.commit()
            # print("query executed")

            # result.append([row[0] for row in cursor.description])
            # for row in cursor.fetchall():
            #     result.append([str(x) for x in row])

            cursor.close()
            # print("cursor closed")
        except Exception as e:
            print(f'{str(e)}')
            # result.append()
            cursor.close()
        # return result

    def close_connection(self):
        try:
            self.pool.release(self.connection)
            print(f"Released connection to:{self.conn_obj.host}")

        except:
            print(f"Could not release connection to:{self.conn_obj.host}, closing pool instead")
            try:
                self.pool.destroy()
            except:
                print(f"{self.conn_obj.name} has a pool that is already inactive")
            print(f"Closed connection to:{self.conn_obj.host}")

    def test_connection(self):
        # Open database connection
        # db = pymysql.connect(credentials['patching_database_host'], credentials['patching_database_user'], credentials['patching_database_password'], config['patching_database_schema'])
        db = pymysql.connect(host=self.conn_obj.host, user=self.conn_obj.credential.username,
                             passwd=decrypt_message(self.conn_obj.credential.password), port=int(self.conn_obj.port),
                             db=json.loads(self.conn_obj.attributes)['schema'])
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        print(f"Created new connection to:{self.conn_obj.host} ")
        # execute SQL query using execute() method.
        cursor.execute("SELECT VERSION()")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Database version : %s " % data)

        # disconnect from server
        db.close()
        print(f"Closed connection to:{self.conn_obj.host}")


class PostgreGreenplumConnector(DatabaseConnector):
    def __init__(self, conn_obj):
        self.conn_obj= conn_obj
    def commit(self):
        pass
    def open_connection(self):

        self.connection = psycopg2.connect(f"dbname={json.loads(self.conn_obj.attributes)['dbname']} user={self.conn_obj.credential.username} password={decrypt_message(self.conn_obj.credential.password)} host={self.conn_obj.host} port={self.conn_obj.port}")



    def run_report(self, report):
        super().run_report(report)


    def execute_query(self, query,**kwargs):
        result=[]
        cursor = self.connection.cursor()
        try:

            # print("cursor opened")
            cursor.execute(query)
            # print("query executed")
            # result.append([row[0] for row in cursor.description])
            result = [[x for x in query.split("from")[0].split("select ")[1].replace(" ","").split(",")]]
            for row in cursor.fetchall():
                result.append([str(x) for x in row])

            cursor.close()
            # print("cursor closed")
        except Exception as e:
            print(f'{str(e)}')
            # result.append()
            cursor.close()
        return result

    def execute_update(self, query,auto_commit=True,**kwargs):
        # result = []

        cursor = self.connection.cursor()
        try:
            # print("cursor opened")

            cursor.execute(query)
            cursor.commit()
            # print("query executed")

            # result.append([row[0] for row in cursor.description])
            # for row in cursor.fetchall():
            #     result.append([str(x) for x in row])

            cursor.close()
            # print("cursor closed")
        except Exception as e:
            print(f'{str(e)}')
            # result.append()
            cursor.close()
        # return result

    def close_connection(self):
        self.connection.close()
    def test_connection(self):
        connection = psycopg2.connect(f"dbname={json.loads(self.conn_obj.attributes)['dbname']} user={self.conn_obj.credential.username} password={decrypt_message(self.conn_obj.credential.password)} hos={self.conn_obj.host} port={self.conn_obj.port}")
        connection.close()
        return True
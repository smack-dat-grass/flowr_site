from .models import SearchSource
from config.classes import OracleConnector, MySQLConnector, LDAPConnector
import traceback,json
from config.models import API_CONNECTOR_TYPE, ORACLE_CONNECTOR_TYPE,LDAP_CONNECTOR_TYPE,MYSQL_CONNECTOR_TYPE
_delimeter="|||"

def run_search(input, object_type):

    search_sources = SearchSource.objects.filter(object_type=object_type)
    results={}
    data={'warnings':[]}
    for source in search_sources:
        try:
            print (source)

            if source.connection.type==MYSQL_CONNECTOR_TYPE:
                mysql_conn = MySQLConnector(source.connection)
                try:
                    mysql_conn.open_connection()
                    if _delimeter in input:
                        for _input in input.split(_delimeter):
                            if source.name not in results:
                                results[source.name]= mysql_conn.execute_query(source.code.replace('?', _input),**json.loads(source.attributes))
                            else:
                                tmp = mysql_conn.execute_query(source.code.replace('?', _input),**json.loads(source.attributes))
                                del tmp[0]
                                results[source.name]+=tmp
                    else:
                        mysql_conn.execute_query(source.code.replace('?', input), **json.loads(source.attributes))
                    mysql_conn.close_connection()
                except Exception as e:
                    data['warnings'].append(f"Could not load results for {source.name}: {e}")
                    mysql_conn.close_connection()

            if source.connection.type==LDAP_CONNECTOR_TYPE:
                ldap_conn = LDAPConnector(source.connection)
                try:
                    ldap_conn.open_connection()
                    if _delimeter in input:
                        for _input in input.split(_delimeter):
                            if source.name not in results:
                                results[source.name] = ldap_conn.execute_query(source.code.replace('?', _input),**json.loads(source.attributes))
                            else:
                                tmp = ldap_conn.execute_query(source.code.replace('?', _input),**json.loads(source.attributes))
                                del tmp[0]
                                results[source.name] +=tmp
                    else:
                        results[source.name] = ldap_conn.execute_query(source.code.replace('?', input),**json.loads(source.attributes))
                    ldap_conn.close_connection()
                except Exception as e:
                    data['warnings'].append(f"Could not load results for {source.name}: {e}")
                    ldap_conn.close_connection()

            if source.connection.type==ORACLE_CONNECTOR_TYPE:
                ora_conn = OracleConnector(source.connection)
                try:
                    ora_conn.open_connection()
                    if _delimeter in input:
                        print(input.split(_delimeter))
                        for _input in input.split(_delimeter):
                            if source.name not in results:
                                # print(f"first results for {source.name} for {_input}")
                                results[source.name]=ora_conn.execute_query(source.code.replace("?",_input), **json.loads(source.attributes), verbose=True)
                            else:
                                # print(f"adding results for {source.name} for {_input}")
                                tmp = ora_conn.execute_query(source.code.replace("?", _input),**json.loads(source.attributes), verbose=True)
                                del tmp[0]
                                results[source.name] +=tmp
                                # print(results)
                    else:
                        results[source.name]=ora_conn.execute_query(source.code.replace("?",input), **json.loads(source.attributes))
                    ora_conn.close_connection()
                except Exception as e:
                    data['warnings'].append(f"Could not load results for {source.name}: {e}")
                    ora_conn.close_connection()

            if source.name in results and len(results[source.name]) >0:
                for i in range(1, len(results[source.name])):

                    entry = {}
                    for ii in range(0, len(results[source.name][i])):
                        entry[results[source.name][0][ii]] = results[source.name][i][ii]
                    if source.name in data:
                        data[source.name].append(entry)
                    else:
                        data[source.name]=[]
                        data[source.name].append(entry)
        except:
            raise Exception(f"{traceback.format_exc()}\n\n\nError occurred running search: {source.name}")
    if len(data.keys()) ==0:
        raise Exception(f"Hmm, we couldn't find any {object_type.name} that matched your query. Please validate \"{input}\" was your intended search and try again.")
    return data
    pass
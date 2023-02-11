# import multiprocessing

import time

from .classes import  *
from django.conf import settings
from .models import API_CONNECTOR_TYPE, ORACLE_CONNECTOR_TYPE,LDAP_CONNECTOR_TYPE,MYSQL_CONNECTOR_TYPE,POSTGRE_CONNECTOR_TYPE
import multiprocessing as mp
mp.set_start_method('fork')
def encrypt(input):
    return input

def decrypt(input):
    return input
def open_connection(connection):
    if connection.type == ORACLE_CONNECTOR_TYPE:  # handle oracle case
        ora_conn = OracleConnector(connection)
        ora_conn.open_connection()

    if connection.type == MYSQL_CONNECTOR_TYPE:
        mysql_conn = MySQLConnector(connection)
        mysql_conn.open_connection()
    if connection.type==LDAP_CONNECTOR_TYPE:
        ldap_conn = LDAPConnector(connection)
        ldap_conn.open_connection()
    if connection.type==POSTGRE_CONNECTOR_TYPE:
        postgre_conn = PostgreGreenplumConnector(connection)
        postgre_conn.open_connection()

def close_connection(connection):
    if connection.name in settings.DATABASE_POOL:
        if connection.type == ORACLE_CONNECTOR_TYPE:  # handle oracle case
            ora_conn = OracleConnector(connection)
            ora_conn.open_connection()
            ora_conn.close_connection()

        if connection.type == MYSQL_CONNECTOR_TYPE:
            mysql_conn = MySQLConnector(connection)
            mysql_conn.open_connection()
            mysql_conn.close_connection()
        if connection.type == LDAP_CONNECTOR_TYPE:
            ldap_conn = LDAPConnector(connection)
            ldap_conn.close_connection()
        if connection.type == POSTGRE_CONNECTOR_TYPE:
            postgre_conn = PostgreGreenplumConnector(connection)
            postgre_conn.close_connection()
def test_connection(connection):
    if connection.type == ORACLE_CONNECTOR_TYPE:  # handle oracle case
        ora_conn = OracleConnector(connection)
        ora_conn.test_connection()

    if connection.type == MYSQL_CONNECTOR_TYPE:
        mysql_conn = MySQLConnector(connection)
        mysql_conn.test_connection()
    if connection.type==LDAP_CONNECTOR_TYPE:
        ldap_conn = LDAPConnector(connection)
        ldap_conn.test_connection()
    if connection.type==POSTGRE_CONNECTOR_TYPE:
        postgre_conn = PostgreGreenplumConnector(connection)
        postgre_conn.test_connection()
def process_list_concurrently(data, process_function, batch_size,kwargs):
    '''
    Process a list concurrently
    :param data: the list to process
    :param process_function: the function to pass to the multiprocessing module
    :param batch_size: the number of records to process at a time
    :return: None
    '''
    start_time = time.time()
    _keys = [x for x in data[1:]]
    n = batch_size
    loads = [_keys[i:i + n] for i in range(0, len(_keys), n)]
    # for load in loads:
    loads[0].insert(0, data[0])
    processes = {}
    for i in range(0, len(loads)):
        load=loads[i]
    # for load in loads:
        print(f"Processing the load {i}/{len(loads)}: "+','.join([str(x) for x in load]))
        p = mp.Process(target=process_function, args=(load,kwargs,),)
        p.start()

        processes[str(p.pid)] = p
    # pids = [x for x in processes.keys()]
    while any(processes[p].is_alive() for p in processes.keys()):
        # print(f"Waiting for {len([x for x in processes if x.is_alive()])} processes to complete. Going to sleep for 10 seconds")
        process_str = ','.join([str(v.pid) for v in processes.values() if v.is_alive()])
        print(f"The following child processes are still running: {process_str}")
        time.sleep(10)
    print(f"\nCompleted in {int((int(time.time()) - start_time) / 60)} minutes and {int((int(time.time()) - start_time) % 60)} seconds")
    # return pids
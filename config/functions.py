from .classes import  *
from django.conf import settings
from .models import API_CONNECTOR_TYPE, ORACLE_CONNECTOR_TYPE,LDAP_CONNECTOR_TYPE,MYSQL_CONNECTOR_TYPE,POSTGRE_CONNECTOR_TYPE
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

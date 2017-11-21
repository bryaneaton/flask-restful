#!/usr/bin/env python


mssql = {'host': 'dbhost',
         'user': 'dbuser',
         'passwd': 'dbPwd',
         'db': 'db'}

postgresql = {'host': 'dbhost',
         'user': 'dbuser',
         'passwd': 'dbPwd',
         'db': 'db'}


mssqlConfig = "mssql+pyodbc://{}:{}@{}:1433/{}?driver=SQL+Server+Native+Client+10.0".format(mssql['user'], mssql['passwd'], mssql['host'], mssql['db'])
postgresqlConfig = "postgresql+psycopg2://{}:{}@{}/{}".format(postgresql['user'], postgresql['passwd'], postgresql['host'], postgresql['db'])

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # SQL lite connection string
# app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://dsuser:dsu3r_123@CTG-SQLLAB01:1433/ITQ?driver=SQL+Server+Native+Client+10.0" #SQL Server Credentials
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://alexis:Alexis2014@localhost/custom"


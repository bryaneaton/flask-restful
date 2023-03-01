#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

mssql = {'host': 'database',
         'user': 'dbuser',
         'passwd': 'dbPwd',
         'db': 'db'}

postgresql = {'host': 'database',
         'user': 'postgres',
         'passwd': 'magical_password',
         'db': 'db'}


mssqlConfig = "mssql+pyodbc://{}:{}@{}:1433/{}?driver=SQL+Server+Native+Client+10.0".format(mssql['user'], mssql['passwd'], mssql['host'], mssql['db'])
postgresqlConfig = "postgresql+psycopg2://{}:{}@{}/{}".format(postgresql['user'], postgresql['passwd'], postgresql['host'], postgresql['db'])


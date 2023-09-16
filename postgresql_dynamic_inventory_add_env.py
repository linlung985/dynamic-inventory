#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import commands
import psycopg2
import json
import os

host = os.environ['HOSTNAME']
ip = os.environ['IP_ADDRESS']

output_dict={}

conn = psycopg2.connect(
    host = "192.168.196.120",
    port = 5000,
    database="postgres",
    user="postgres",
    password="password")

cursor = conn.cursor()

insert_groups_tbl_data = "INSERT INTO groups VALUES ( 'web' );"
insert_hosts_tbl_data = "INSERT INTO hosts VALUES ( '" + host + "', 'web' );"
insert_hostvars_tbl_data = "INSERT INTO hostvars VALUES ( '" + host + "', 'ansible_host', '" + ip + "');"

cursor.execute(insert_groups_tbl_data)
cursor.execute(insert_hosts_tbl_data)
cursor.execute(insert_hostvars_tbl_data)

conn.commit()
cursor.close()
conn.close()

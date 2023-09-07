#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import commands
import psycopg2
import json

output_dict={}

# DBコネクションの定義
conn = psycopg2.connect(
#    host = commands.getoutput('sudo podman inspect --format "{{ .NetworkSettings.IPAddress }}" postgres'),
    host = "192.168.196.120",
#    port = 5432,
    port = 5000,
    database="postgres",
    user="postgres",
    password="password")

cur_group = conn.cursor()
cur_group.execute("""SELECT groupname FROM groups""")

# グループごとに辞書を作成して追加する
for row_group in cur_group:
    group_dict={}
    grouphosts=[]
    groupvars={}

    cur_hosts = conn.cursor()
    cur_hosts.execute("""SELECT hostname FROM hosts WHERE groupname = %s""", (row_group[0],))

    for row_host in cur_hosts:
        grouphosts.append(row_host[0])

    cur_groupvars = conn.cursor()
    cur_groupvars.execute("""SELECT varname, varvalue FROM groupvars WHERE groupname = %s""", (row_group[0],))

    for row_groupvar in cur_groupvars:
        groupvars[row_groupvar[0]]=row_groupvar[1]

    group_dict["hosts"]=grouphosts
    group_dict["vars"]=groupvars
    output_dict[row_group[0]]=group_dict

cur_hosts = conn.cursor()
cur_hosts.execute("""SELECT DISTINCT hostname FROM hosts""")

meta_dict={}
hostvars={}

# ホストごとに辞書を作成して追加する
for row_host in cur_hosts:
    hostvar={}

    cur_hostvars = conn.cursor()
    cur_hostvars.execute("""SELECT varname,varvalue FROM hostvars WHERE hostname = %s""", (row_host[0],))

    for row_hostvar in cur_hostvars:
        hostvar[row_hostvar[0]]=row_hostvar[1]

    hostvars[row_host[0]]=hostvar

meta_dict["hostvars"]=hostvars
output_dict["_meta"]=meta_dict

# 辞書をJSON形式して標準出力する
print json.dumps(output_dict, indent=4)


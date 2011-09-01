#!/usr/bin/python
#coding:utf8
from dbutils import DB
import settings

def cleanup():
    db = DB()
    db.decrease_pwd_tries()
    db.remove_inactive_users()
    


if __name__ == '__main__':
    cleanup()

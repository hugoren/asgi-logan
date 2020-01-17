"""
Author: Hugo
Date: 2020-01-15 21:02
Desc: 
"""

from peewee import Model
from peewee import (CharField,
      IntegerField, TextField
     )
from peewee import SqliteDatabase

db = SqliteDatabase("logan.db")


class Info(Model):
    name = CharField()
    age = IntegerField()

    class Meta:
        database = db


class AuditModel(Model):
    event = TextField()
    event_type = CharField(null=True)
    level = IntegerField()
    timestamp = CharField()

    class Meta:
        database = db
        table_name = 'audit'


def create_table(table):
    db.create_tables([table,])


def save():
    info_instance = Info(name="hugo", age=18)
    info_instance.save()


if __name__ == "__main__":
    db.connect()
    create_table(AuditModel)

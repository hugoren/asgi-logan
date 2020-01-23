"""
Author: Hugo
Date: 2020-01-15 20:49
Desc:
"""

import click
from passlib.context import CryptContext


@click.group()
def init():
    pass


@init.command()
@click.option('--env', default='dev', help='please into env')
def init_env(env):
    print(env)


@init.command()
@click.option('--db_name', default="logan", help='db name')
def init_db(db_name):
    print(db_name)


@init.command()
@click.option('--table_name', prompt='table name', help='custom table name')
def init_create(table_name):
    print(table_name)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@init.command()
@click.option('--password', prompt='please input password', help='please input password')
def password_hash(password):
    pwd_hash = pwd_context.hash(password)
    print(pwd_hash)
    return pwd_hash


cli = click.CommandCollection(sources=[init])


if __name__ == '__main__':
    cli()



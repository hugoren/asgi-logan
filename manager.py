"""
Author: Hugo
Date: 2020-01-15 20:49
Desc:
"""

import click


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


cli = click.CommandCollection(sources=[init])


if __name__ == '__main__':
    cli()



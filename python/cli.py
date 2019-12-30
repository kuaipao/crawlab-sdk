import os
from getpass import getpass

import click

import constants
from core.client import client
from core.config import config


@click.group()
def cli():
    pass


@click.command('login', help='login to the platform and get token')
@click.option('--username', '-u')
@click.password_option('--password', '-p', confirmation_prompt=False)
@click.option('--api_address', '-a')
def login(username=None, password=None, api_address=None):
    if username is not None:
        config.data.username = username
    if password is not None:
        config.data.password = password
    if api_address is not None:
        config.data.api_address = api_address
    config.save()
    client.update_token()


@click.command('config', help='set config info')
@click.option('--username', '-u')
@click.password_option('--password', '-p', confirmation_prompt=False)
@click.option('--api_address', '-a')
def config_(username=None, password=None, api_address=None):
    if username is not None:
        config.data.username = username
    if password is not None:
        config.data.password = password
    if api_address is not None:
        config.data.api_address = api_address
    config.save()
    print('config has been saved')


@click.command('check', help='check the connection and update token')
def check():
    client.update_token()


@click.command('nodes', help='list the nodes')
def nodes():
    client.list_nodes()


@click.command('spiders', help='list the spiders')
def spiders():
    client.list_spiders()


@click.command('schedules', help='list the schedules')
def schedules():
    client.list_schedules()


@click.command('tasks', help='list the tasks')
@click.option('--number', '-n', help='number of tasks')
def tasks(number=None):
    client.list_tasks(number)


@click.command('upload', help='upload a spider')
@click.option('--type', '-t', default=constants.Spider.CUSTOMIZED, help='spider type')
@click.option('--directory', '-d', help='directory path, for customized spiders')
@click.option('--name', '-n', help='spider name')
@click.option('--col', '-c', help='spider results collection')
@click.option('--display_name', '-N', help='spider display name')
@click.option('--command', '-m', help='spider execution command')
@click.option('--id', '-i', help='spider id')
@click.option('--spiderfile', '-f', help='Spiderfile path')
def upload(type=None, directory=None, name=None, col=None, display_name=None, command=None, id=None, spiderfile=None):
    # TODO: finish all functionality
    if type is None:
        type = constants.Spider.CUSTOMIZED

    if type == constants.Spider.CUSTOMIZED:
        # customized spider
        if directory is None:
            directory = os.path.abspath(os.curdir)
            client.upload_customized_spider(directory, name, col, display_name,  command, id)
    elif type == constants.Spider.CONFIGURABLE:
        # configurable spider
        pass


if __name__ == '__main__':
    cli.add_command(check)
    cli.add_command(config_)
    cli.add_command(login)
    cli.add_command(nodes)
    cli.add_command(schedules)
    cli.add_command(tasks)
    cli.add_command(spiders)
    cli.add_command(upload)

    cli()

#!/usr/bin/env python3

import click
from Repository import Repository

repository = None

@click.group()
def cli():
    global repository
    if repository is None:
        repository = Repository()

@click.command()
def init():
    print("Initializing repository...")
    repository.init()

@click.command()
@click.argument('file_name', type=click.Path())
def add(file_name):
    print(f"Adding file: {file_name}...")
    repository.add(file_name)

@click.command()
@click.argument('message', type=click.STRING)
def commit(message):
    print(f"Committing with message: '{message}'...")
    repository.commit(message)

@click.command()
def status():
    print("Checking repository status...")
    repository.status()

@click.command()
def log():
    print("Retrieving commit log...")
    repository.log()

@click.command()
@click.argument('hash_commit', type=click.STRING)
def checkout(hash_commit):
    print(f"Checking out commit: {hash_commit}...")
    repository.checkout(hash_commit)

@click.command()
def push():
    print("Pushing the files for review...")
    repository.push()


cli.add_command(init)
cli.add_command(add)
cli.add_command(commit)
cli.add_command(status)
cli.add_command(log)
cli.add_command(checkout)
cli.add_command(push)

if __name__ == '__main__':
    print("in my CLI...")
    cli()


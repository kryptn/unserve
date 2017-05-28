import click

from unserve import build_handler

@click.command()
@click.argument('module')
def handle(module):
    handler = build_handler(module)
    handler()

if __name__ == '__main__':
    handle()

import click

from unserve import build_handler

@click.command()
@click.argument('module')
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000)
def handle(module, host, port):
    handler = build_handler(module, host, port)
    handler()

if __name__ == '__main__':
    handle()

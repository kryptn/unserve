import click

from unserve import build_handler


@click.command()
@click.argument('module')
@click.option('--host', default='0.0.0.0')
@click.option('--port', default=5000)
@click.option('--hot-reload', default=False)
def handle(module, host, port, hot_reload):
    handler = build_handler(module, host, port, hot_reload)
    handler()


if __name__ == '__main__':
    handle()

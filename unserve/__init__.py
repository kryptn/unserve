import re
import importlib

import yaml

from sanic import Sanic
from sanic.response import HTTPResponse


class Handler:
    module = None

    def __init__(self, path, hot_reload=False):
        self.path = path
        if hot_reload:
            self.handler = self.reloader
        else:
            self.handler = self.build_handler()

    def __call__(self, *args, **kwargs):
        return self.handler(*args, **kwargs)

    def _import(self, path):
        name, fn = re.match('^(.*)\.(.*)$', path).groups()

        if self.module:
            importlib.reload(self.module)
        else:
            self.module = importlib.import_module(name)

        return getattr(self.module, fn)

    def build_handler(self):
        fn = self._import(self.path)

        def handler(*args, **kwargs):
            return fn(*args, **kwargs)
        return handler

    def reloader(self, *args, **kwargs):
        fn = self.build_handler()
        return fn(*args, **kwargs)


def get_functions(module_name, config_file='serverless.yml'):
    path = '{}/{}'.format(module_name, config_file)
    with open(path) as fd:
        config = yaml.load(fd)
    return config['functions']


def build_function(fn):
    def handeled(*args, **kwargs):
        # FIXME This needs to conform the sanic request
        # FIXME to the aws lambda event object
        # TODO context needs to be mocked here
        # signature for aws lambda handers is fn(event, context)
        if len(args) < 2:
            args = tuple([*args, None])
        response = fn(*args, **kwargs)
        return HTTPResponse(response['body'],
                            response['statusCode'],
                            content_type="application/json")
    return handeled


def build_route(module_name, lambda_fn, hot_reload):

    handler_name = list(lambda_fn.keys())[0]
    handler_fn_name = lambda_fn[handler_name]['handler']

    # try to import the function
    path = '{}.{}'.format(module_name, handler_fn_name)

    fn = build_function(Handler(path, hot_reload))

    # there's probably a better way to handle this
    route = '/'
    methods = ['GET']
    if 'events' in lambda_fn[handler_name]:
        if 'http' in lambda_fn[handler_name]['events']:
            http = lambda_fn[handler_name]['events']['http']
            if 'path' in http:
                route += http['path']
            if 'method' in http:
                methods = [http['method'].upper()]

    # set up args, kwargs signature
    return (fn, route), {'methods': methods}


def build_app(module_name, functions, hot_reload):
    app = Sanic()
    for key, value in functions.items():
        args, kwargs = build_route(module_name, {key: value}, hot_reload)
        app.add_route(*args, **kwargs)

    return app


def build_handler(module_name, host, port, hot_reload):
    functions = get_functions(module_name)

    app = build_app(module_name, functions, hot_reload)

    return lambda: app.run(host=host, port=port)

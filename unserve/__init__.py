import re

import yaml
from sanic import Sanic
from sanic.response import HTTPResponse

def _import(module, fn_name):
    # import the target handler
    mod = __import__(module, fromlist=[fn_name])
    return getattr(mod, fn_name)

def get_functions(module_name, config_file='serverless.yml'):
    path = '{}/{}'.format(module_name, config_file)
    with open(path) as fd:
        config = yaml.load(fd)
    return config['functions']

def hot_reload(fn):
    # TODO this might be easy
    return fn

def build_function(fn):
    def handeled(*args, **kwargs):
        # FIXME This needs to conform the sanic request
        # FIXME to the aws lambda event object
        # TODO context needs to be mocked here
        # signature for aws lambda handers is fn(event, context)
        if len(args) < 2:
            args = tuple([*args, None])
        response = fn(*args, **kwargs)
        return HTTPResponse(response['body'], response['statusCode'], 
                            content_type="application/json")
    return handeled

def build_route(module_name, lambda_fn):

    handler_name = list(lambda_fn.keys())[0]
    handler_fn_name = lambda_fn[handler_name]['handler']

    # split up the module and the function
    # 'a.b.c.d' => ('a.b.c', 'd')
    path = '{}.{}'.format(module_name, handler_fn_name)
    module, fn_name = re.compile('^(.*)\.(.*)$').match(path).groups()

    # try to import the function
    fn = _import(module, fn_name)

    # plug in hot reloading TODO stubbed tho
    hot_fn = hot_reload(build_function(fn))

    # there's probably a better way to handle this
    route = '/'
    methods = ['GET']
    if 'events' in lambda_fn[handler_name]:
        if 'http' in lambda_fn[handler_name]['events']:
            if 'path' in lambda_fn[handler_name]['events']['http']:
                route += lambda_fn[handler_name]['events']['http']['path']
            if 'method' in lambda_fn[handler_name]['events']['http']:
                methods = [lambda_fn[handler_name]['events']['http']['method'].upper()]

    # set up args, kwargs signature
    return (hot_fn, route), {'methods':methods}

def build_app(module_name, functions):
    app = Sanic()
    for key, value in functions.items():
        args, kwargs = build_route(module_name, {key: value})
        app.add_route(*args, **kwargs)
    
    return app

def build_handler(module_name, host, port):
    functions = get_functions(module_name)

    app = build_app(module_name, functions)

    return lambda: app.run(host=host, port=port)


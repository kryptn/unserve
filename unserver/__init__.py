import re

import yaml
from sanic import Sanic
from sanic.response import HTTPResponse


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

    # there's probably a better way to handle this
    route = '/'
    methods = ['GET']
    if 'events' in lambda_fn[handler_name]:
        if 'http' in lambda_fn[handler_name]['events']:
            if 'path' in lambda_fn[handler_name]['events']['http']:
                route += lambda_fn[handler_name]['events']['http']['path']
            if 'method' in lambda_fn[handler_name]['events']['http']:
                methods = [lambda_fn[handler_name]['events']['http']['method'].upper()]

    # try to import the function
    mod = __import__(module, fromlist=[fn_name])
    fn = getattr(mod, fn_name)

    # set up args, kwargs signature
    return (build_function(fn), route), {'methods':methods}

def build_app():
    pass

def build_handler(module_name):
    functions = get_functions(module_name)

    app = Sanic()

    for key, value in functions.items():
        args, kwargs = build_route(module_name, {key: value})
        app.add_route(*args, **kwargs)

    app.run(host='0.0.0.0', port=5000)


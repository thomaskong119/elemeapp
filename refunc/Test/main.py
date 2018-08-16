# -*- coding: utf-8 -*-

import refunc
from refunc import Context, Message


def on_request(ctx: Context, payload: dict):
    pass


if __name__ == '__refunc_dev__':
    # run using:
    # refunc-dev main.py

    import refunc
    from refunc.util import enable_logging

    # setup mock
    enable_logging()
    # set mock endpoint
    refunc.current_env().context.set_mock_endpoint('ci-test/test')

    # add extra mock points, for example:
    # comment out the following lines, a function at "foo/bar" can be mocked
    #
    # current_env().context.add_mock_func('foo/bar', lambda c, kv: kv)

    def simple_test(**kwargs: dict):
        return refunc.invoke("ci-test/test", **kwargs)

    try:
        from IPython import embed
        __name__ = '__main__'  # fix warning
        embed()
    except:
        print("cannot drop into ipython, exec simple_test")
        print(simple_test())

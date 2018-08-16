# -*- coding: utf-8 -*-

import refunc
from refunc import Context, Message

import json
import urllib.request

dingurl = 'https://oapi.dingtalk.com/robot/send?access_token=549961be9efed1a4a1c56318e3480834521ad64920f9d7e29263dbb4bb0d30a8'
header = {'Content-Type': 'application/json'}

def on_request(ctx: Context, payload: dict):
    content = payload.pop("content", "")
    mobilelist = payload.pop("mobilelist", "")
    # mobilelist = "18600536524"
    dingdata = {
        "msgtype": "text",
        "text": {"content": content},
        "at": {"atMobiles": [mobilelist], "isAtAll": False},
    }
    json_str = json.dumps(dingdata).encode('utf8')
    dingreq = urllib.request.Request(dingurl, data=json_str, headers=header)
    dingres = urllib.request.urlopen(dingreq)
    ctx.log(dingres)


if __name__ == '__refunc_dev__':
    # run using:
    # refunc-dev main.py

    import refunc
    from refunc.util import enable_logging

    # setup mock
    enable_logging()
    # set mock endpoint
    refunc.current_env().context.set_mock_endpoint('appleoperation/dingmsgservice')

    # add extra mock points, for example:
    # comment out the following lines, a function at "foo/bar" can be mocked
    #
    # current_env().context.add_mock_func('foo/bar', lambda c, kv: kv)

    def simple_test(**kwargs: dict):
        return refunc.invoke("appleoperation/dingmsgservice", **kwargs)

    try:
        from IPython import embed

        __name__ = '__main__'  # fix warning
        embed()
    except:
        print("cannot drop into ipython, exec simple_test")
        print(simple_test())

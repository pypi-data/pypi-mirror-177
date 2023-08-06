""" API from OpenAPI for Cloudflare API"""

import sys
import datetime
import json

def do_path(path):
    """ do_path() """

    cmds = []
    action = ''
    deprecated = False
    deprecated_date = ''
    deprecated_already = False
    v = {'action': action, 'cmd': cmd, 'deprecated': deprecated, 'deprecated_date': deprecated_date, 'deprecated_already': deprecated_already}
    cmds.append(v)

def api_decode_from_openapi(content):
    """ API decode from OpenAPI for Cloudflare API"""

    try:
        j = json.loads(content)
        components = j['components']
        info = j['info']
        openapi = j['openapi']
        paths = j['paths']
        servers = ['servers']
    except Exception as e:
        sys.stderr.write("OpenAPI read: %s\n" % (e))
        return None

    all_cmds = []
    for path in paths:
        all_cmds += do_path(section)

    return sorted(all_cmds, key=lambda v: v['cmd'])

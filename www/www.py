import os
import subprocess
import pathlib
import responder
import json

ROOT = "{}/wwwroot".format(os.environ['SNAP'])
DATA = os.environ['SNAP_DATA']

api = responder.API(
    static_dir="{}/static".format(ROOT),
    templates_dir="{}/templates".format(ROOT),
)

api.add_route("/static/", static=True)

def get_config(val):
    stdout, stderr = subprocess.Popen(["snapctl", "get", val],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()
    return stdout.decode('utf-8').strip()

def set_config(key, val):
    stdout, stderr = subprocess.Popen(["snapctl", "set", "{}=\"{}\"".format(key, val)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()
    if stderr:
        return False
    return True

@api.route("/")
async def index(req, resp):
    resp.html = api.template('index.html')

@api.route("/{page}")
async def index(req, resp, *, page):
    resp.html = api.template("{}.html".format(page))

@api.route("/api/config")
async def config(req, resp):

    if req.method == "get":
        values = [
            "domains",
            "dkim-domains",
            "postfix-domain",
            "postfix-origin",
            "postfix-relay-host",
            "use-snakeoil-cert",
            "haproxy-username",
            "haproxy-password"
        ]
        config = {}
        for val in values:
            config[val] = get_config(val)
        resp.media = { "config": config }
    elif req.method == "post":

        data = await req.media()
        log = []
        for upd in data['update']:
            log.append("Set {} to {}".format(upd['key'], upd['value']))
            set_config(upd['key'], upd['value'])

        resp.media = {
            "success": True,
            "log": log
        }
    else:
        resp.media = {"success": False}

@api.route("/api/ansible")
async def ansible(req, resp):
    if req.method == "get":
        with open("{}/provision.log".format(DATA)) as f:
            data = f.read()
        try:
            json_data = json.loads(data)
        except:
            json_data = {}
        resp.media = {"data": json_data}
    elif req.method == "post":
        pathlib.Path("{}/do-provision".format(DATA)).touch(exist_ok=True)
        resp.media = {"success": True}
    else:
        resp.media = {"success": False}

def main():
    api.run()

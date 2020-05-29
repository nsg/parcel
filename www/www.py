import os
import random
import string
import subprocess
import pathlib
import responder
import json
import yaml
import socket
import dns.resolver
import requests

def get_config(val):
    stdout, stderr = subprocess.Popen(["snapctl", "get", val],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()
    o = stdout.decode('utf-8').strip()
    return yaml.load(o)

def set_config(key, val):
    if ',' in val:
        val = "[{}]".format(val)

    stdout, stderr = subprocess.Popen(["snapctl", "set", "{}=\"{}\"".format(key, val)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()
    if stderr:
        return False
    return True

ROOT = "{}/wwwroot".format(os.environ['SNAP'])
DATA = os.environ['SNAP_DATA']
SECRET_TOKEN = get_config("www-token")
SNAP_REVISION = os.environ['SNAP_REVISION']

MENU = [
    {"name": "Welcome", "url": "/", "id": "index"},
    {"name": "Configure", "url": "/configure/", "id": "configure"},
    {"name": "Status", "url": "/status/", "id": "status"},
]

api = responder.API(
    static_dir="{}/static".format(ROOT),
    static_route="/static/{}".format(SNAP_REVISION),
    templates_dir="{}/templates".format(ROOT),
)

@api.route("/")
async def index(req, resp):
    if req.headers.get('TOKEN') == SECRET_TOKEN:
        resp.html = api.template('index.html',
            menu=MENU,
            current="/",
            page="index",
            static_hash=SNAP_REVISION)
    else:
        resp.text = "Error: You need to provide a correct TOKEN"

@api.route("/{page}")
async def page(req, resp, *, page):
    if req.headers.get('TOKEN') != SECRET_TOKEN:
        resp.text = "Error: You need to provide a correct TOKEN"
        return

    norm_page = page.replace("/", "")
    valid_pages = [x['id'] for x in MENU]
    if norm_page in valid_pages:
        resp.html = api.template(
            "{}.html".format(norm_page),
            menu=MENU,
            current="/{}/".format(norm_page),
            page=norm_page,
            static_hash=SNAP_REVISION
        )
    else:
        resp.text = "404: Page not found"
        resp.status_code = 404

@api.route("/api/config")
async def config(req, resp):
    if req.headers.get('TOKEN') != SECRET_TOKEN:
        resp.media = {"message": "Error: You need to provide a correct TOKEN"}
        return

    if req.method == "get":
        values = [
            "domains",
            "origin",
            "relay-host",
            "use-snakeoil-cert",
            "haproxy-username",
            "haproxy-password",
            "lxd-remote",
            "lxd-password",
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
    if req.headers.get('TOKEN') != SECRET_TOKEN:
        resp.media = {"message": "Error: You need to provide a correct TOKEN"}
        return

    if req.method == "get":
        with open("{}/provision.log".format(DATA)) as f:
            data = f.read()
        try:
            json_data = json.loads(data)
        except:
            json_data = {}

        running = pathlib.Path("{}/do-provision".format(DATA)).exists()
        resp.media = {
            "data": json_data,
            "running": running
        }
    elif req.method == "post":
        pathlib.Path("{}/do-provision".format(DATA)).touch(exist_ok=True)
        resp.media = {"success": True}
    else:
        resp.media = {"success": False}

@api.route("/api/validate")
async def validate(req, resp):
    if req.headers.get('TOKEN') != SECRET_TOKEN:
        resp.media = {"message": "Error: You need to provide a correct TOKEN"}
        return

    if req.method == "post":
        req_data = await req.media()
        field = req_data['field']
        data = req_data['data']
        msg = []

        if field == "origin":
            if not is_resolve(data):
                msg.append("Lookup of {} failed".format(data))

        elif field == "domains":
            for d in data.split(","):
                try:
                    for x in dns.resolver.query(d, 'MX'):
                        if not is_resolve(x.exchange.to_text()):
                            msg.append(f"The MX record for {d} points to {x.exchange.to_text()}, lookup failed!")
                except dns.resolver.NoAnswer:
                    msg.append(f"No MX records found for {d}. You need to add one or more MX records to the domain.")
                except dns.resolver.NXDOMAIN:
                    msg.append(f"Lookup of {d} failed, domain not found.")

        resp.media = msg

def is_resolve(domain):
    try:
        socket.gethostbyname(domain)
    except Exception:
        return False
    return True

def main():
    api.run()

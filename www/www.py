import os
import random
import string
import subprocess
import pathlib
import responder
import json

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

def gen_example_pass():
    letters = string.ascii_lowercase \
        + string.ascii_uppercase \
        + "0123456789_-"
    p = []
    for _ in range(16):
        p.append(random.choice(letters))
    return ''.join(p)

ROOT = "{}/wwwroot".format(os.environ['SNAP'])
DATA = os.environ['SNAP_DATA']
SECRET_TOKEN = get_config("www-token")

MENU = [
    {"name": "Welcome", "url": "/", "id": "index"},
    {"name": "Configure", "url": "/configure/", "id": "configure"},
    {"name": "Stats", "url": "/stats/", "id": "stats"},
    {"name": "Provision", "url": "/provision/", "id": "provision"},
]

api = responder.API(
    static_dir="{}/static".format(ROOT),
    templates_dir="{}/templates".format(ROOT),
)

api.add_route("/static/", static=True)

@api.route("/")
async def index(req, resp):
    if req.headers.get('TOKEN') == SECRET_TOKEN:
        resp.html = api.template('index.html', menu=MENU, current="/", page="index")
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
            example_password=gen_example_pass()
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
            "postfix-relay-host",
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

def main():
    api.run()

import os
import responder

ROOT = "{}/wwwroot".format(os.environ['SNAP'])

api = responder.API(
    static_dir="{}/static".format(ROOT),
    templates_dir="{}/templates".format(ROOT),
)

api.add_route("/static/", static=True)

@api.route("/")
async def index(req, resp):
    resp.html = api.template('index.html')

def main():
    api.run()

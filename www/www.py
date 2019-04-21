import os
import responder

ROOT = "{}/wwwroot".format(os.environ['SNAP'])

api = responder.API(
    static_dir="{}/static".format(ROOT),
    templates_dir="{}/templates".format(ROOT),
)

@api.route("/{greeting}")
async def greet_world(req, resp, *, greeting):
    resp.text = f"{greeting}, world!"

def main():
    api.run()

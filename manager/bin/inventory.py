#!/usr/bin/env python3

import json
import sys
import argparse
import subprocess

CONF_VALUES = [
        "domains",
        "origin",
        "relay_host",
        "use_snakeoil_cert",
        "haproxy_username",
        "haproxy_password",
        "www_token"
    ]

def parse_json(data):
    try:
        ret = json.loads(data)
    except ValueError:
        return False
    return ret

def get_conf(param):
    param = param.replace('_','-')
    out = subprocess.check_output(["snapctl", "get", param]).decode("utf-8")

    # If it's a list, parse it as JSON
    if out[:1] == "[":
        # Turn [foo,bar] to ["foo","bar"]
        json_out = out.replace("[", "[\"").replace("]", "\"]").replace(",", "\",\"")
        json_ret = parse_json(json_out)
        if json_ret:
            return json_ret
    return noyes(out.strip())

def noyes(s):
    if s in ["no", "false", "False"]:
        return False
    if s in ["yes", "true", "True"]:
        return True
    return s

def get_inventory_vars():
    out = {}
    for v in CONF_VALUES:
        out[v] = get_conf(v)
    return out

def main(argv):
    parser = argparse.ArgumentParser(description='Ansible Inventory System')
    parser.add_argument('--list', help='List all inventory groups', action="store_true")
    parser.add_argument('--host', help='List vars for a host')
    args = parser.parse_args()

    if args.list:
        inventory_vars = get_inventory_vars()
        data = {"all": {"vars": inventory_vars}}
        print(json.dumps(data, indent=2))
    if args.host:
        print(json.dumps({}))

if __name__ == '__main__':
    sys.exit(main(sys.argv))

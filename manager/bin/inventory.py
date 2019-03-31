#!/usr/bin/env python3

import json
import sys
import argparse
import subprocess

CONF_VALUES = [
        "domains",
        "postfix_domain",
        "postfix_origin",
        "postfix_relay_host",
    ]

def get_conf(param):
    param = param.replace('_','-')
    try:
        out = subprocess.check_output(["snapctl", "get", param]).decode("utf-8")
    except subprocess.CalledProcessError:
        return False
    if out.strip():
        ret = out.strip().split(",")
        if len(ret) > 1:
            return ret
        return ret[0]
    return False

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

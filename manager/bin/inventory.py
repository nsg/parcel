#!/usr/bin/env python3

import json
import sys
import argparse
import subprocess

CONF_VALUES = [
        ("domains", list),
        ("origin", str),
        ("relay_host", bool),
        ("use_snakeoil_cert", bool),
        ("haproxy_username", str),
        ("haproxy_password", str),
        ("lxd_method", str),
        ("lxd_remote", str),
        ("lxd_password", str),
        ("www_token", str),
    ]

def get_conf(param, param_type):
    param = param.replace('_','-')
    out = subprocess.check_output(["snapctl", "get", param]).decode("utf-8")

    if (param_type == str):
        return out.strip()
    elif (param_type == bool):
        return noyes(out.strip())
    elif (param_type == list):
        ret = out.strip().split(",")
        if len(ret) > 1:
            return ret
        try:
            return json.loads(ret[0])
        except ValueError:
            return ret
    return ""

def noyes(s):
    if s in ["no", "false", "False"]:
        return False
    if s in ["yes", "true", "True"]:
        return True
    return s

def get_inventory_vars():
    out = {}
    for v,t in CONF_VALUES:
        out[v] = get_conf(v, t)
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

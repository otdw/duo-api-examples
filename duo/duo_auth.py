#!/usr/bin/env python

#Checks various endpoints in duo auth_api. methods are defined in:
#https://duo.com/docs/authapi#endpoints
#
#Use help option to see required parameters.

import sys, csv, argparse, getpass, yaml
import duo_client
from six.moves import input

__author__ = "David Woodruff"

def check_auth(auth_api):
    time =  auth_api.check()
    print ''
    print "Response: "
    print "=========="
    print(yaml.safe_dump(time, default_flow_style=False))

def duo_auth(pargs, auth_api):
    args = []
    kwargs = {}
    auth = auth_api.auth(pargs.factor,username=pargs.user,device='auto',\
        *args,**kwargs)
    print ''
    print "Response: "
    print "=========="
    print(yaml.safe_dump(auth, default_flow_style=False))

def preauth(pargs, auth_api):
    print "Checking Preauth details ..."
    print "============================"
    preauth = auth_api.preauth(username=pargs.user)
    print ''
    print "Response: "
    print "=========="
    print(yaml.safe_dump(preauth, default_flow_style=False))

def auth_stat(pargs, auth_api):
    args = []
    kwargs = {}
    for user in pargs.user:
        txid = auth_api.auth(pargs.factor,username=user,\
            device='auto',async='1',*args,**kwargs).values()
        print ''
        print "Checking auth status for txid: ", txid
        print "======================================"
        auth_stat = auth_api.auth_status(txid)
        print ''
        print "Response: "
        print "=========="
        print(yaml.safe_dump(auth_stat, default_flow_style=False))

def main():
    parser = argparse.ArgumentParser(
        description="Check Authentication Params to DUO.")
    parser.add_argument("--ikey", help="Integration Key")
    parser.add_argument("host", help="API Hostname [api-xx.duosecurity.com]")
    parser.add_argument("--method", help="API Method")
    parser.add_argument("--user", nargs='+', help="Username")
    parser.add_argument("--factor", help="2FA Factor [push, sms, phone]")

    pargs = parser.parse_args()

    skey = getpass.getpass("API Secret key:")

    auth_api = duo_client.Auth(pargs.ikey, skey, pargs.host)

    if not pargs.factor and "check" not in pargs.method:
        raise RuntimeError('Must provide factor')

    elif 'check' in pargs.method:
        check_auth(auth_api)
    elif 'auth' in pargs.method:
        duo_auth(pargs, auth_api)
    elif 'preauth' in pargs.method:
        preauth(pargs, auth_api)
    elif 'stat' in pargs.method:
        auth_stat(pargs, auth_api)
    else:
        raise RuntimeError('Invalid Method')

if __name__ == "__main__":
    main()

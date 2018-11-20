import base64
import datetime
import email
import json
import os
import re
import subprocess
from virus_total_apis import PublicApi as vtapi
from virus_total_apis import PrivateApi as vtapi_priv

import eml_parser

cwd = os.getcwd()

API_KEY = 'Sign-Up for API Key at virustotal.com'

PUBLICAPI=True

try:
    API_KEY = os.environ["VT_API_KEY"]
except Exception as apikeyproblem:
    pass

try:
    API_KEY = os.environ["VT_PRIV_API_KEY"]
    PUBLICAPI=False
except Exception as apikeyproblem:
    pass

with open("URL_WHITELIST.txt","r") as f:
    whitelist = [line.rstrip('\n') for line in f]


def get_urls(body):
    regexstr = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
    urls = re.findall(regexstr, body)
    defanged = []
    for url in urls:
        if url not in whitelist:
            defanged.append(url.replace("https://","hxxps://").replace("http://","hxxp://"))
    defanged = set(defanged)
    return defanged

def get_vt_url_score(url):
    if(API_KEY == 'Sign-Up for API Key at virustotal.com'):
        return "No API Key Specified.  Specify as environment variable \"VT_API_KEY\" when running dockerfile"
    else:
        retstr = ""
        vt = vtapi(API_KEY)
        response = vt.get_url_report(url)
        results = json.dumps(response)
        retstr+="("+str(type(results))+")"
        #return json.dumps(response, sort_keys=False)
        return retstr


def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


def dumpemail(eml):
    with open(eml, 'rb') as fhdl:
        raw_email = fhdl.read()

    with open(eml, 'r', encoding="utf-8") as fhdl:
        emldump = fhdl.read()

    parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)

    subj = parsed_eml.get("header").get("subject")
    subj = str(subj)
    frm = parsed_eml.get("header").get("from")
    frm = str(frm)
    to = parsed_eml.get("header").get("to")
    to = str(to)
    rcvd = parsed_eml.get("header").get("received")[len(parsed_eml.get("header").get("received"))-1]
    rcvd = str(rcvd)

    b = email.message_from_string(emldump)
    ploads = []
    if b.is_multipart():
        for payload in b.get_payload():
            #if payload.is_multipart():
            p = str(payload.get_payload()).replace("\n","").rstrip()
            try:
                p = base64.b64decode(p)
            except Exception as problem:
                p="could not decode: "+ str(problem)
            ploads.append(p)
    else:
        p = str(b.get_payload()).replace("\n","").rstrip()
        try:
                p = p = base64.b64decode(p)
        except Exception as problem:
            p="could not decode: "+ str(problem)
        ploads.append(p)

    urls = get_urls(str(ploads))
    urltable = ""
    if(len(urls)>0):
        #urls = str(urls)
        urltable+="<table>"
        urltable+="<tr>"
        urltable+="<td>URL</td>"
        urltable+="<td>VT Score</td>"
        urltable+="</tr>"
        for url in urls:
            urltable+="<tr>"
            urltable+="<td>"+str(url)+"</td>"
            if(len(urls)<=4 or PUBLICAPI is False):
                urltable+="<td>"+str(get_vt_url_score(url))+"</td>"
            else:
                urltable+="<td>Public API only allows for 4 requests per minute</td>"
            urltable+="</tr>"
        urltable+="</table>"
    else:
        #urls="None found."
        urltable="None found."

    details = "<table class='table'>"

    details+="<tr>"
    details+="<td>Subject</td>"
    details+="<td>"+subj+"</td>"
    details+="</tr>"

    details+="<tr>"
    details+="<td>From</td>"
    details+="<td>"+frm+"</td>"
    details+="</tr>"

    details+="<tr>"
    details+="<td>To</td>"
    details+="<td>"+to+"</td>"
    details+="</tr>"

    details+="<tr>"
    details+="<td>Sender Information (from 'Received' Headers)</td>"
    details+="<td><code>"+rcvd+"</code></td>"
    details+="</tr>"

    details+="<tr>"
    details+="<td>URLs</td>"
    details+="<td>"+urltable+"</td>"
    details+="</tr>"
    
    details+="</table>"

    return details

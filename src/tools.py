import datetime
import json
import eml_parser
import subprocess
import os
cwd = os.getcwd()

import re

def get_urls(body):
    urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', body)
    defanged = []
    for url in urls:
        defanged.append(url.replace("https://","hxxps://").replace("http://","hxxp://"))
    return defanged


def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


def dumpemail(eml):
    with open(eml, 'rb') as fhdl:
        raw_email = fhdl.read()

    parsed_eml = eml_parser.eml_parser.decode_email_b(raw_email)

    subj = parsed_eml.get("header").get("subject")
    subj = str(subj)
    frm = parsed_eml.get("header").get("from")
    frm = str(frm)
    to = parsed_eml.get("header").get("to")
    to = str(to)
    rcvd = parsed_eml.get("header").get("received")[len(parsed_eml.get("header").get("received"))-1]
    rcvd = str(rcvd)
    urls = get_urls(str(parsed_eml.get("body")))
    urls = str(urls)

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
    details+="<td>"+urls+"</td>"
    details+="</tr>"
    
    details+="</table>"

    # tmp debug

    #details+="<br><br>"+str(parsed_eml)

    #return (json.dumps(parsed_eml, default=json_serial))
    return details

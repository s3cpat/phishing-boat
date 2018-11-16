import datetime
import json
import eml_parser
import subprocess
import os
cwd = os.getcwd()

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

    details = "<table class='table'>"

    details+="<tr>"
    details+="<td>Subject</td>"
    details+="<td>"+subj+"</td>"
    details+="</tr>"

    details+="<tr>"
    details+="<td>From</td>"
    details+="<td>"+frm+"</td>"
    details+="</tr>"
    
    details+="</table>"

    # tmp debug

    # details+="<br><br>"+str(parsed_eml.get("header"))

    #return (json.dumps(parsed_eml, default=json_serial))
    return details

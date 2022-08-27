import json
import os

from flask import render_template

def applications_table():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           "../../", 
                           "application_list.json"), "r") as fh:
        ret = render_template("main/i_applist.jinja2", 
                              applist = json.load(fh))
    return ret
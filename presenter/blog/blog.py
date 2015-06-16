from flask import Blueprint, Response, request, session, render_template

from playhouse.flask_utils import object_list

from .models import Entry

import urllib

blog = Blueprint("blog", __name__, template_folder="templates")


def clean_querystring(request_args, *keys_to_remove, **new_values):
    querystring = dict((key, value) for key, value in request_args.items())
    for key in keys_to_remove:
        querystring.pop(key, None)

    querystring.update(new_values)

    return urllib.urlencode()


@blog.route("/")
def blog_index():
    query = Entry.public().order_by(Entry.timestamp.desc())

    return object_list("blog_index.html", query)

blog.add_app_template_filter(clean_querystring, "clean_querystring")

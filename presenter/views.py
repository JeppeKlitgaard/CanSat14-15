"""
Contains the views and routes used by the Flask-webserver.
"""

from flask import (render_template, send_from_directory, Response, session,
                   redirect, request, url_for, flash)

from .app import app

import os
import functools

from playhouse.flask_utils import object_list, get_object_or_404

from .models import Entry

from .logic import get_static_graph_data, get_global_data_config


# pylint: disable=unused-argument
@app.errorhandler(404)
def not_found(exc):
    """
    Called when a resource could not be found - a 404 has been raised.
    """
    return Response("<h3>Not found</h3>"), 404
# pylint: enable=unused-argument


def login_required(fn):
    """
    A decorator to be used on routes that require the user to be logged in.
    """
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        """
        The inner function of the decorator.
        """
        if session.get("logged_in"):
            return fn(*args, **kwargs)
        return redirect(url_for("login", next=request.path))
    return inner


@app.context_processor
def dropdown_processor():
    """
    Context processor that makes the get_dropdown_data function
    available to all templates.
    """
    def get_dropdown_data():
        """
        Returns dropdown data.
        """
        return get_global_data_config()
    return dict(get_dropdown_data=get_dropdown_data)


@app.route("/favicon.ico")
def favicon():
    """
    Route in charge of finding the favicon.ico.
    """
    return send_from_directory(os.path.join(app.root_path, "static", "img"),
                               "favicon.ico",
                               mimetype="image/vnd.microsoft.icon")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Route for logging in.
    """
    next_url = request.args.get("next") or request.form.get("next")

    if request.method == "POST" and request.form.get("password"):
        password = request.form.get("password")
        if password == app.config["ADMIN_PASSWORD"]:
            session["logged_in"] = True
            session.permanent = True
            flash("You are now logged in.", "success")
            return redirect(next_url or url_for("index"))
        else:
            flash("Incorrect password.", "danger")

    return render_template("login.html", next_url=next_url)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    """
    Route for logging out.
    """
    if request.method == "POST":
        session.clear()
        return redirect(url_for("login"))

    return render_template("logout.html", page_title="Log out")


@app.route("/about")
def about():
    """
    Renders the about page.
    """
    return render_template("about.html", page_title="About")


@app.route("/")
@app.route("/index")
def index():
    """
    Renders the index page.
    """
    return render_template("index.html")


@app.route("/live")
def live():
    """
    Renders the live page.
    """
    return render_template("live.html", replay_available=False,
                           page_title="Live")


@app.route("/map")
def map():
    """
    Renders a live map page.
    """
    return render_template("map.html", page_title="Map")


@app.route("/graph/<data_id>")
def graph(data_id):
    """
    Renders the graph page using a ``data_id``.
    """
    json_data = get_static_graph_data(data_id, force=True)

    return render_template("graph.html", graph_data=json_data, data_id=data_id,
                           replay_available=True, page_title="Graph")


@app.route("/replay/<data_id>")
def replay(data_id):
    """
    Renders the replay page using a ``data_id``.
    """
    return render_template("replay.html", data_id=data_id, page_title="Replay")


@app.route("/blog/")
@app.route("/blog/index")
def blog_index():
    """
    Renders the index of the blog.
    """
    query = Entry.public().order_by(Entry.timestamp.desc())

    return object_list("blog_index.html", query, check_bounds=False,
                       page_title="Blog")


@app.route("/blog/create", methods=["GET", "POST"])
@login_required
def blog_create():
    """
    Renders the 'create an entry' page for the blog.
    """
    if request.method == "POST":
        if request.form.get("title") and request.form.get("content"):
            # pylint: disable=no-member
            entry = Entry.create(
                title=request.form["title"],
                content=request.form["content"],
                published=request.form.get("published") or False)
            # pylint: enable=no-member
            flash("Entry created successfully.", "success")
            if entry.published:
                return redirect(url_for("blog_detail", slug=entry.slug))
            else:
                return redirect(url_for("blog_edit", slug=entry.slug))
        else:
            flash("Title and Content are required.", "danger")
    return render_template("blog_create.html", page_title="Create blog entry")


@app.route("/blog/drafts")
@login_required
def blog_drafts():
    """
    Renders a page with entry drafts.
    """
    query = Entry.draft().order_by(Entry.timestamp.desc())

    return object_list("blog_index.html", query, check_bounds=False,
                       page_title="Drafts")


@app.route("/blog/detail/<slug>")
@app.route("/blog/<slug>")
def blog_detail(slug):
    """
    Renders a blog entry.
    """
    if session.get("logged_in"):
        # pylint: disable=no-member
        query = Entry.select()
        # pylint: enable=no-member
    else:
        query = Entry.public()
    entry = get_object_or_404(query, Entry.slug == slug)
    return render_template("blog_detail.html", entry=entry,
                           page_title=entry.title)


@app.route("/blog/<slug>/edit", methods=["GET", "POST"])
@login_required
def blog_edit(slug):
    """
    Renders the edit page of a blog entry.
    """
    entry = get_object_or_404(Entry, Entry.slug == slug)
    if request.method == "POST":
        if request.form.get("title") and request.form.get("content"):
            entry.title = request.form["title"]
            entry.content = request.form["content"]
            entry.published = request.form.get("published") or False
            entry.save()

            flash("Entry saved successfully.", "success")
            if entry.published:
                return redirect(url_for("blog_detail", slug=entry.slug))
            else:
                return redirect(url_for("blog_edit", slug=entry.slug))
        else:
            flash("Title and Content are required.", "danger")

    return render_template("blog_edit.html", entry=entry,
                           page_title="Edit entry")

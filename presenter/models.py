import datetime
import re

from .app import flask_db, oembed_providers, app

from peewee import *
from playhouse.sqlite_ext import *

from flask import Markup

from micawber import parse_html

from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension


class Entry(flask_db.Model):
    title = CharField()
    slug = CharField(unique=True)
    content = TextField()
    published = BooleanField(index=True)
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)

    @property
    def html_content(self):
        """
        Generate HTML representation of the markdown-formatted blog entry,
        and also convert any media URLs into rich media objects such as video
        players or images.
        """
        hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
        extras = ExtraExtension()
        markdown_content = markdown(self.content, extensions=[hilite, extras])
        oembed_content = parse_html(
            markdown_content,
            oembed_providers,
            urlize_all=True,
            maxwidth=app.config['SITE_WIDTH'])
        return Markup(oembed_content)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = re.sub(r'[^\w)]+', r'-', self.title.lower())
        ret = super(Entry, self).save(*args, **kwargs)

        return ret

    @classmethod
    def public(cls):
        return Entry.select().where(Entry.published == True)

    @classmethod
    def draft(cls):
        return Entry.select().where(Entry.published == False)

"""
Contains the database models used by the presenter module.
"""

import datetime
import re

from .app import flask_db, oembed_providers, app

from peewee import CharField, TextField, BooleanField, DateTimeField

from flask import Markup

from micawber import parse_html

from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension


class Entry(flask_db.Model):
    """
    Represents a basic blog entry.
    """
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
        """
        Saves the entry to the database.
        """
        if not self.slug:
            # pylint: disable=no-member
            self.slug = re.sub(r'[^\w)]+', r'-', self.title.lower())
            # pylint: enable=no-member
        ret = super(Entry, self).save(*args, **kwargs)

        return ret

    @classmethod
    def public(cls):
        """
        Returns the published entries.
        """
        # pylint: disable=no-member
        return Entry.select().where(Entry.published == True)  # noqa comparison
        # pylint: enable=no-member

    @classmethod
    def draft(cls):
        """
        Returns the drafts among the entries.
        """
        # pylint: disable=no-member
        return Entry.select().where(Entry.published == False)  # noqa comparison
        # pylint: enable=no-member

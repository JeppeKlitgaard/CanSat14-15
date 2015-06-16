import datetime
import re

from ..app import flask_db, database

from peewee import *
from playhouse.sqlite_ext import *


class Entry(flask_db.Model):
    title = CharField()
    slug = CharField(unique=True)
    content = TextField()
    published = BooleanField(index=True)
    timestamp = DateTimeField(default=datetime.datetime.now, index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = re.sub(r'[^\w)]+', r'-', self.title.lower())
        ret = super(Entry, self).save(*args, **kwargs)

        self.update_search_index()

        return ret

    def update_search_index(self):
        try:
            fts_entry = FTSEntry.get(FTSEntry.entry_id == self.id)
        except FTSEntry.DoesNotExist:
            fts_entry = FTSEntry(entry_id=self.id)
            force_insert = True
        else:
            force_insert = False

        fts_entry.content = "\n".join((self.title, self.content))
        fts_entry.save(force_insert=force_insert)

    @classmethod
    def public(cls):
        return Entry.select().where(Entry.published == True)

    @classmethod
    def draft(cls):
        return Entry.select().where(Entry.published == False)

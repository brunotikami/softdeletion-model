"""
From Adrienne's Medium post [0]:

The pieces:

* `delete` — bulk deleting a QuerySet bypasses an individual object’s delete method, which is why this is needed here as well

* `alive` and `dead` are just helpers — you may find you don’t need them.

* `hard_delete`, as above, actually removes the objects from your database, but does this on a QuerySet instead of an individual object

[0] https://adriennedomingus.medium.com/soft-deletion-in-django-e4882581c340
"""

from datetime import datetime


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=datetime.utcnow())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)
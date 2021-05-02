"""
From Adrienne's Medium post [0]:

The pieces:

* We initialize with `alive_only` set to True by default, unless we’ve instantiated the manager with that in the `kwargs``
(by calling `all_objects` instead of `objects`)


* We define `get_queryset` that, unless we’re calling `all_objects` returns any object that doesn’t have a value for `deleted_at`
— you don’t want to be working with things your users think they’ve deleted! Otherwise, just return everything, using the 
`SoftDeletionQuerySet`, which we’ll look at below

* `hard_delete`, once again allows us to really truly delete a thing.

[0] https://adriennedomingus.medium.com/soft-deletion-in-django-e4882581c340
"""

from django.db import models

from softdeletion.querysets import SoftDeletionQuerySet


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()
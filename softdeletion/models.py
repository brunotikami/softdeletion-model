"""
From Adrienne's Medium post [0]:

The pieces:

* `deleted_at`: this means that all models inheriting from the SoftDeletionModel will have this attribute available to be set. 
                By default it will be null. I recommend a date instead of a boolean so that you can create a background job that 
                hard-deletes any objects that were “deleted” more than 24 hours/7 days/30 days (whatever the right cadence is for 
                you and your users ) ago — data that users choose to delete should actually be deleted.

* We’ll look at objects and all_objects in the next section. This is what makes this so powerful

* `abstract = True`: This just means we won’t ever define a SoftDeletionModel object on its own. More detail from the Django docs here [1].

* The `delete` method means that whenever you call `.delete()` on any object that inherits from the `SoftDeletionModel`, it won’t 
actually be deleted from the database — its deleted_at attribute will be set instead

* `hard_delete` gives you the option to really truly delete something from the database if you want to, but is named something other 
than the usual delete methods to ensure that you have to think about what you’re doing before you do it, and actually mean to do it. 
This usually won’t be exposed to users, but could only be called by developers from the shell.

[0] https://adriennedomingus.medium.com/soft-deletion-in-django-e4882581c340
[1] https://docs.djangoproject.com/en/1.11/topics/db/models/#abstract-base-classes
"""

from softdeletion.managers import SoftDeletionManager


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = datetime.utcnow()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete() 
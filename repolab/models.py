from django.db import models


class Repository(models.Model):
    path = models.CharField(max_length=1024)
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % self.name

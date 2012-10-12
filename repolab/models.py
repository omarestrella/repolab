from django.db import models
from django.template.defaultfilters import slugify

import vcs


class Repository(models.Model):
    path = models.CharField(max_length=1024)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=64, unique=True)

    def save(self):
        self.slug = slugify(self.name)
        super(Repository, self).save()

    @property
    def root(self):
        repo = vcs.get_repo(path=self.path)
        return repo.get_changeset().get_node('')

    def __unicode__(self):
        return u'%s' % self.name

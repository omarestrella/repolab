from django.db import models
from django.template.defaultfilters import slugify

import vcs

from repolab import repoutils


class Repository(models.Model):
    path = models.CharField(max_length=1024)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=64, unique=True)

    def save(self):
        self.slug = slugify(self.name)
        super(Repository, self).save()

    def get_repo_nodes(self, changeset=None, node=''):
        repo = vcs.get_repo(path=self.path)
        nodes = repo.get_changeset(changeset).get_node(node)
        for dirnode in nodes:
            if not dirnode.is_dir():
                continue
            dirnode.last_changeset = repoutils.dir_get_last_changeset(dirnode)
        return nodes

    @property
    def root(self):
        return self.get_repo_nodes()

    @property
    def branches(self):
        """
        Return the repository's branches as an OrderedDict
        """
        repo = vcs.get_repo(path=self.path)
        return repo.branches

    class Meta:
        verbose_name_plural = "repositories"

    def __unicode__(self):
        return u'%s' % self.name

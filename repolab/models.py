from itertools import imap

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

    def get_repo(self):
        return vcs.get_repo(path=str(self.path))

    def get_repo_nodes(self, changeset=None, node=''):
        repo = self.get_repo()
        nodes = repo.get_changeset(changeset).get_node(node)
        if nodes.is_file():
            return nodes
        else:
            for dirnode in nodes:
                if not dirnode.is_dir():
                    continue
                dirnode.last_changeset = repoutils.dir_get_last_changeset(dirnode)
            return nodes

    @models.permalink
    def get_absolute_url(self):
        return ('repo_url', (self.slug,), {})

    @property
    def root(self):
        return self.get_repo_nodes()

    @property
    def branches(self):
        """
        Return the repository's branches as an OrderedDict
        """
        return self.get_repo().branches

    @property
    def changesets(self):
        """
        Return all the repository's changesets as a generator of changesets.
        """
        return self.get_repo().get_changesets()

    @property
    def default_branch(self):
        return self.get_repo().DEFAULT_BRANCH_NAME

    def has_changeset(self, changeset_hash):
        all_changesets = self.get_repo().get_changesets()
        return changeset_hash in imap(lambda x: x.raw_id, all_changesets)

    class Meta:
        verbose_name_plural = "repositories"

    def __unicode__(self):
        return u'%s' % self.name

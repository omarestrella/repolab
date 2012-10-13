from django.conf import settings
from django.views.generic import TemplateView, ListView, DetailView

import vcs

from repolab import models
from repolab import repoutils


class Homepage(ListView):
    model = models.Repository
    template_name = 'repolab/homepage.html'
    context_object_name = 'repos'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)

        repo = vcs.get_repo(path=settings.GIT_REPO_PATH)
        context['root'] = repo.get_changeset().get_node('')

        return context


class ViewRepo(DetailView):
    model = models.Repository
    template_name = 'repolab/repository/repo.html'
    context_object_name = 'repo'

    def get_context_data(self, **kwargs):
        context = super(ViewRepo, self).get_context_data(**kwargs)

        context['nodes'] = self.object.root.nodes

        # Add last_changeset to dir nodes
        for dirnode in context['nodes']:
            if not dirnode.is_dir(): continue
            dirnode.last_changeset = repoutils.dir_get_last_changeset(dirnode)

        return context


class ViewChangeset(TemplateView):
    template_name = 'repolab/node.html'

    def get_context_data(self, **kwargs):
        context = super(ViewChangeset, self).get_context_data(**kwargs)

        repo = vcs.get_repo(path=settings.GIT_REPO_PATH)
        context['root'] = repo.get_changeset(self.kwargs['changeset']).get_node('')

        return context

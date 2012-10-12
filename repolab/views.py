from django.conf import settings
from django.views.generic import TemplateView

import vcs


class Homepage(TemplateView):
    template_name = 'repolab/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)

        repo = vcs.get_repo(path=settings.GIT_REPO_PATH)
        context['root'] = repo.get_changeset().get_node('')

        return context


class ViewChangeset(TemplateView):
    template_name = 'repolab/node.html'

    def get_context_data(self, **kwargs):
        context = super(ViewChangeset, self).get_context_data(**kwargs)

        repo = vcs.get_repo(path=settings.GIT_REPO_PATH)
        context['root'] = repo.get_changeset(self.kwargs['changeset']).get_node('')

        return context

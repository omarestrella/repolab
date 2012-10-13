from django.http import Http404
from django.views.generic import TemplateView, ListView, DetailView

from repolab import models


class Homepage(ListView):
    model = models.Repository
    template_name = 'repolab/homepage.html'
    context_object_name = 'repos'


class ViewRepo(DetailView):
    model = models.Repository
    template_name = 'repolab/repository/repo.html'
    context_object_name = 'repo'

    def get_context_data(self, **kwargs):
        context = super(ViewRepo, self).get_context_data(**kwargs)

        context['nodes'] = self.object.root.nodes
        return context


class ViewChangeset(ViewRepo):
    template_name = 'repolab/repository/repo.html'

    def get_context_data(self, **kwargs):
        context = super(ViewChangeset, self).get_context_data(**kwargs)
        repo = self.object
        changeset = self.kwargs.get('changeset', None)

        # Need to check if the changeset is a branch or not
        branch = repo.branches.get(changeset, None)
        if branch:
            changeset = repo.branches[changeset]
        else:
            raise Http404
        context['nodes'] = repo.get_repo_nodes(changeset=changeset)
        return context


class EditChangesetPath(TemplateView):
    pass


class ViewChangesetCommit(TemplateView):
    pass

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from repolab import models


class ChangesetMixin(object):
    def get_changeset(self, *args, **kwargs):
        changeset = self.kwargs.get('changeset', None)
        repo = get_object_or_404(models.Repository, slug=self.kwargs.get('slug', None))

        # If changeset is a branch name, use latest changeset from that branch
        if changeset in repo.branches:
            changeset = repo.branches[changeset]

        elif not repo.has_changeset(changeset):
            raise Http404

        return changeset


class RepoMixin(object):
    def get_repo(self, *args, **kwargs):
        return get_object_or_404(models.Repository, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = {}
        repo = self.get_repo()
        context['changeset'] = self.kwargs.get('changeset', repo.default_branch)
        return context


class Homepage(ListView):
    model = models.Repository
    template_name = 'repolab/homepage.html'
    context_object_name = 'repos'


class ViewRepo(DetailView, RepoMixin):
    model = models.Repository
    template_name = 'repolab/repository/nodes.html'
    context_object_name = 'repo'

    def get_context_data(self, **kwargs):
        context = super(ViewRepo, self).get_context_data(**kwargs)
        context.update(RepoMixin.get_context_data(self, **kwargs))
        context['nodes'] = self.get_repo().root
        return context


class ViewChangesetPath(DetailView, RepoMixin, ChangesetMixin):
    model = models.Repository
    template_name = 'repolab/repository/nodes.html'
    context_object_name = 'repo'

    def get_context_data(self, **kwargs):
        context = super(ViewChangesetPath, self).get_context_data(**kwargs)
        context.update(RepoMixin.get_context_data(self, **kwargs))
        repo = self.get_repo()
        changeset = self.get_changeset()
        context['nodes'] = repo.get_repo_nodes(changeset=changeset, node=self.kwargs.get('path'))
        context['path'] = self.kwargs.get('path')
        return context


class EditChangesetPath(TemplateView):
    pass


class ViewChangesetCommit(TemplateView):
    pass

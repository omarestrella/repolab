from django.http import Http404
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from repolab import models


class RepoMixin(object):

    def get_repo(self, *args, **kwargs):
        return get_object_or_404(models.Repository, slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = {}
        repo = self.get_repo()
        context['changeset'] = self.kwargs.get('changeset', repo.default_branch)
        return context

    def get_breadcrumbs(self, path, changeset_name=None):
        '''
        Give a list of breadcrumbs.  Each breadcrumb is a dict with a `name`
        and `url`.
        '''
        repo = self.get_repo()
        path = filter(lambda x: x, map(escape, path.split('/')))
        changeset_name = changeset_name or self.kwargs.get('changeset') or repo.default_branch

        breadcrumbs = []

        if changeset_name == repo.default_branch:
            root_url = reverse_lazy('repo_url', kwargs={
                'slug': repo.slug,
            })
        else:
            root_url = reverse_lazy('repo_changeset_url', kwargs={
                'slug': repo.slug,
                'changeset': changeset_name,
            })
        breadcrumbs.append({
            'name': repo.name,
            'url': mark_safe(root_url),
        })

        for i, directory in enumerate(path):
            breadcrumbs.append({
                'name': directory,
                'url': mark_safe(reverse_lazy('repo_path_url', kwargs={
                    'slug': repo.slug,
                    'changeset': changeset_name,
                    'path': '/'.join(path[0:i+1]),
                })),
            })

        return breadcrumbs


class ChangesetMixin(RepoMixin):

    def get_changeset(self, *args, **kwargs):
        changeset = self.kwargs.get('changeset', None)
        repo = get_object_or_404(models.Repository, slug=self.kwargs.get('slug', None))

        # If changeset is a branch name, use latest changeset from that branch
        if changeset in repo.branches:
            changeset = repo.branches[changeset]

        elif not repo.has_changeset(changeset):
            raise Http404

        return changeset


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
        context['breadcrumbs'] = self.get_breadcrumbs('')

        return context


class ViewChangesetPath(DetailView, ChangesetMixin):
    model = models.Repository
    template_name = 'repolab/repository/nodes.html'
    context_object_name = 'repo'

    def get_context_data(self, **kwargs):
        context = super(ViewChangesetPath, self).get_context_data(**kwargs)
        context.update(RepoMixin.get_context_data(self, **kwargs))
        repo = self.get_repo()
        changeset = self.get_changeset()

        nodes = repo.get_repo_nodes(changeset=changeset, node=self.kwargs.get('path'))
        context['nodes'] = nodes

        # Adjust template name based on type of node
        if nodes.is_file():
            self.template_name = 'repolab/repository/file.html'

        context['path'] = self.kwargs.get('path')
        context['breadcrumbs'] = self.get_breadcrumbs(context['path'])

        return context


class EditChangesetPath(TemplateView):
    pass


class ViewChangesetCommit(TemplateView):
    pass


class ListChangesets(DetailView, RepoMixin):
    model = models.Repository
    template_name = 'repolab/repository/changeset_list.html'
    context_object_name = 'repo'

    def get_context_data(self, **kwargs):
        context = super(ListChangesets, self).get_context_data(**kwargs)
        context.update(RepoMixin.get_context_data(self, **kwargs))
        repo = self.get_repo()

        all_changesets = list(repo.changesets)
        all_changesets.reverse()

        # Paginate
        paginator = Paginator(all_changesets, 20)
        page_num = self.request.GET.get('page')
        try:
            changesets = paginator.page(page_num)
        except PageNotAnInteger:
            # Default to first page
            changesets = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), give last page of results.
            changesets = paginator.page(paginator.num_pages)

        context['changesets'] = changesets
        context['paginator'] = paginator

        return context

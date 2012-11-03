from django import forms

from repolab import models


class RepoForm(forms.ModelForm):
    """
    Form for the `Repo` model
    """

    class Meta:
        model = models.Repository
        exclude = ('slug',)

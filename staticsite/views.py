# -*- coding: utf-8 -*-

from django.views.generic import TemplateView
from django.http import Http404
from django.template import loader, TemplateDoesNotExist
from django.conf import settings
from importlib import import_module

def get_context_map(settings):
    try:
        helper_module_name = settings.STATICSITE_CONTEXT_HELPER_MODULE
    except AttributeError:
        return {}

    # Failure beyond here is a configuration error.
    # - If you define a helper module it must exist and expose the context_map attribute.
    helper_module = import_module(helper_module_name)
    return helper_module.context_map

CONTEXT_MAP = get_context_map(settings)

DEFAULT_INDEX = 'index.html'
STATICSITE_TEMPLATE_DIR = 'staticsite/'

#### Notes
# 1. Currently breaking APPEND_SLASHES. So DEBUG only. (which is probably fine)
# 2. If we can solve 1, then WRITE_TO_DIR with a Warning if the file already exists.
#       — i.e. the idea is to have the web server serve the file.
#       Writing it once is OK. Writing it again-and-again implies a
#       configuration error.
# 3. How do I clean the URL patterns so I can just include('staticsite.urls') ?

class StaticSiteTemplateView(TemplateView):

    def normalised_url(self):
        the_url = self.kwargs['url']

        if the_url == '': the_url = DEFAULT_INDEX
        if the_url.endswith('/'): the_url += DEFAULT_INDEX

        return the_url

    def get_template_names(self):
        template_name = STATICSITE_TEMPLATE_DIR + self.normalised_url()

        # http://stackoverflow.com/questions/5690213/how-to-check-if-a-template-exists-in-django
        #
        # Q: is there a better way of handling this by subclassing
        # TemplateResponse, and assigning that as the view's
        # response_class?
        # <https://docs.djangoproject.com/en/1.5/ref/template-response/#django.template.response.TemplateResponse>
        try:
            loader.get_template(template_name)
        except TemplateDoesNotExist:
            raise Http404

        return [template_name,]

    def get_context_data(self, **kwargs):
        context = super(StaticSiteTemplateView, self).get_context_data(**kwargs)

        if self.normalised_url() in CONTEXT_MAP:
            context.update(CONTEXT_MAP[self.normalised_url()])

        return context

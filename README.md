Django staticsite
=================

**Django static site generator for DEBUG and production.**

**Author:** Carlton Gibson, [Follow me on Twitter][1].

Overview
========

Django staticsite looks to solve the following problems:

* You want to build a static website leveraging Django (templates and all).
* You want your static site to integrate with your existing Django application.
* The [flatpages app](https://docs.djangoproject.com/en/dev/ref/contrib/flatpages/) isn't really for you.

You install Django staticsite. Pages are built per-request in development. You run a management command to build the site as part of your deployment process.

Sounds good? Read on!

Installation
============

Download from PyPy:

    pip install django-staticsite

Update your settings:

    # Add static site to installed apps
    INSTALLED_APPS = (
        ...
        'staticsite',
        ...
    )

    # Provide the absolute path to the folder you will serve the site from.
    #   - Typically this will correspond to your web server's site root setting.
    STATICSITE_OUTPUT_DIR = '/var/www'

Create `staticsite` template dir — as child of a directory appearing in your `TEMPLATE_DIRS` setting.

Update URL Conf:

    from staticsite.views import StaticSiteTemplateView

    # Other URL settings here...

    # Put this last...
    if settings.DEBUG:
        urlpatterns = urlpatterns + patterns('',
            # Catchall — will be passed to staticsite
            #   Note: This breaks APPEND_SLASHES so we're only using it in DEBUG mode...
            url(r'^(?P<url>.*)$', StaticSiteTemplateView.as_view(), name='staticsite'),
        )

You're now good to go!

Usage
=====

##Development##
In development you use `./manage.py runserver` as normal.

Any URLs not already matched will be passed to Django staticsite. Staticsite will search the `staticsite` template directory for a template matching the request URL path. On a match Django staticsite will render the template and return the response. Otherwise it will raise an `HTTP404`.

Notes:

1. Django staticsite assumes directory index templates — those for URLs ending with a `/` — are named `index.html`.
2. The catchall URL breaks APPEND_SLASHES so we only enable it when DEBUG==TRUE — We assume you can handle getting the URLs right there yourself.

I'd like to be able to enable Django staticsite in production too — that way we could serve the static file if it already existed and generate it — whilst writing it to the filesystem for next time — if not. If you know how to do this without breaking APPEND_SLASHES [please open an issue](https://github.com/carltongibson/django-staticsite/issues/new).

## Per-URL Contexts ##

To enable per-URL contexts define a `STATICSITE_CONTEXT_HELPER_MODULE` setting. If defined, the referenced
module must exist and must expose a `context_map` attribute.

`context_map` must be a dictionary-like object mapping URL path fragments — such as `index.html` to a context
dictionary that will be passed to the template for rendering.

The `STATICSITE_CONTEXT_HELPER_MODULE` may employ _Any Means™_ to generate the `context_map`.


##Deployment/Production##

As part of your deployment script run the management command to build the static site:

    ./manage.py --settings=my_project.settings.production buildstaticsite

This will write the site to the path you specified in the `STATICSITE_OUTPUT_DIR` setting.

Beyond that you need to configure your web server to server the static site files if they exist and proxy everything else back to Django.

An example of this for Nginx might look like:

    upstream app_server {
        server 127.0.0.1:8000 fail_timeout=0;
    }

    location @proxy_to_app {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass   http://app_server;
    }

    location / {
        # checks for static file, if not found proxy to app
        try_files $uri/index.html $uri @proxy_to_app;
    }

Enjoy!

Issues Etc
==========

Please use [the issues features here on GitHub](https://github.com/carltongibson/django-staticsite/issues).


Running the tests
=================

To run the tests against the current environment:

    ./manage.py test

Changelog
=========

0.2.0
-----

* Added option to use per-URL context map.


0.1.0
-----

* Initial release

License
=======

Copyright © Carlton Gibson.

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

[1]: http://twitter.com/carltongibson

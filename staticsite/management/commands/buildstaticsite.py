# -*- coding: utf-8 -*-
import os
import codecs

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template import Template, Context
from django.template.loader import get_template

### Notes
#   Expects `staticsite` folder to exist in `settings.TEMPLATE_DIRS`
#       This COULD use Template Loaders.
#
#   Uses `settings.STATICSITE_OUTPUT_DIR` for write location.
#       MAYBE make this a command line argument.
#
#   TODO: Set STATIC_URL context variable from settings.
#   TODO: Render the view here. (Take advantage of get_context_data)
#   TODO: Cache templates so we only write changed files.
#           - c.p. django.contrib.staticfiles collectstatic
class Command(BaseCommand):
    help = 'Writes (HTML) files for templates in staticsite template dir.'

    def handle(self, *args, **options):
        staticsite_dir = self._staticsite_dir()
        output_dir = settings.STATICSITE_OUTPUT_DIR

        for dirpath, subdirs, filenames in os.walk(staticsite_dir):
                for name in filenames:
                    if name.startswith('.'):
                        continue # Put this in for OS X's .DS_Store files.
                                 # TODO: Think about this.

                    # get template and render
                    template_path = os.path.join(dirpath, name)
                    print "Loading template at: %s" % template_path

                    t = get_template(template_path)
                    html = t.render(Context({'STATIC_URL':'/static/'}))

                    # and write
                    write_dir = dirpath.replace(staticsite_dir, output_dir, 1)
                    if not os.path.exists(write_dir):
                        os.makedirs(write_dir)
                    write_path = os.path.join(write_dir, name)

                    write_file = codecs.open(write_path, encoding='utf-8', mode='w')
                    write_file.write(html)
                    write_file.close()

                    print "Wrote: %s" % write_path


    def _staticsite_dir(self):
        for template_dir in settings.TEMPLATE_DIRS:
            for path in os.listdir(template_dir):
                if path == 'staticsite':
                    staticsite_dir = os.path.join(template_dir, path)
                    self.stdout.write('Building staticsite from %s' % staticsite_dir)
                    return staticsite_dir
        raise CommandError('staticsite dir not found in settings.TEMPLATE_DIRS')

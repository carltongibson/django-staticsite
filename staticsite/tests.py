from django.test import TestCase, RequestFactory

from views import StaticSiteTemplateView


class TestURLNormalisation(TestCase):

    def test_empty_path_results_in_index_html(self):
        kwargs = {
            'url':"",
        }

        theView = StaticSiteTemplateView(kwargs=kwargs)

        normalised_url = theView.normalised_url()

        self.assertEquals('index.html', normalised_url)

    def test_directory_index_is_correctly_expanded(self):
        kwargs = {
            'url':"directory/",
        }

        theView = StaticSiteTemplateView(kwargs=kwargs)

        normalised_url = theView.normalised_url()

        self.assertEquals('directory/index.html', normalised_url)

    def test_full_paths_are_unaltered(self):
        kwargs = {
            'url':"directory/subdirectory/real_file.html",
        }

        theView = StaticSiteTemplateView(kwargs=kwargs)

        normalised_url = theView.normalised_url()

        self.assertEquals('directory/subdirectory/real_file.html', normalised_url)

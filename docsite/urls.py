"""docsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url

# Uncomment to enable the Django Admin
# from django.contrib import admin

from staticsite.views import StaticSiteTemplateView

urlpatterns = [
#    Uncomment to enable the Django Admin
#    url(r'^admin/', admin.site.urls),

]

# staticsite catch-all URL. This should go last.
if settings.DEBUG:
    urlpatterns = urlpatterns + [
        # Passed to staticsite. Note: This breaks APPEND_SLASHES
        url(r'^(?P<url>.*)$', StaticSiteTemplateView.as_view(), name='staticsite'),
    ]
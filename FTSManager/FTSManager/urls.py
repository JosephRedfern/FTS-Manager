"""FTSManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.urls import re_path as url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import events.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    url(r'^accounts/profile/$', events.views.me, name='profile'),
    url(r'^$', events.views.home, name='home'),
    url(r'^about/', events.views.about, name='about'),
    url(r'^events/$', events.views.events, name='events'),
    url(r'^events/(?P<event_id>[0-9]+)/$', events.views.event, name='event'),
    url(r'^events/(?P<event_id>[0-9]+)/edit/$', events.views.edit_event, name='edit-event'),
    url(r'^add-event/', events.views.add_event, name='add-event'),
    url(r'^me/', events.views.me, name='my-profile'),
    url(r'^users/(?P<username>\w+)/$', events.views.user, name='user'),
    url(r'^user-autocomplete/$', events.views.UserAutocomplete.as_view(), name='user-autocomplete'),
    url(r'^events.ics$', events.views.EventFeed(), name="calendar-feed"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

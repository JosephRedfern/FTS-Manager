from menu import Menu, MenuItem
from django.core.urlresolvers import reverse

Menu.add_item("main", MenuItem("Home",
                               reverse("events.home")))

# preferences.py
#
# Change the look of Adwaita, with ease
# Copyright (C) 2022  Gradience Team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import os

from gi.repository import GLib, Gio, Gtk, Adw

from .constants import rootdir, app_id
from .modules.flatpak_overrides import create_gtk4_user_override, remove_gtk4_user_override
from .modules.utils import buglog


@Gtk.Template(resource_path=f"{rootdir}/ui/preferences.ui")
class GradiencePreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = "GradiencePreferencesWindow"
    
    allow_flatpak_theming_user = Gtk.Template.Child()
    allow_flatpak_theming_global = Gtk.Template.Child()

    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)

        self.parent = parent
        self.settings = parent.settings

        self.setup()

    def setup(self):
        self.set_search_enabled(False)

        self.setup_flatpak_group()
        
    def setup_flatpak_group(self):
        user_flatpak_theming = self.settings.get_boolean("user-flatpak-theming")
        #global_flatpak_theming = self.settings.get_boolean("global-flatpak-theming")

        self.allow_flatpak_theming_user.set_state(user_flatpak_theming)
        #self.allow_flatpak_theming_global.set_state(global_flatpak_theming)

        self.allow_flatpak_theming_user.connect("state-set", self.on_allow_flatpak_theming_user_toggled)
        #self.allow_flatpak_theming_global.connect("state-set", self.on_allow_flatpak_theming_global_toggled)


    def on_allow_flatpak_theming_user_toggled(self, *args):
        state = self.allow_flatpak_theming_user.props.state

        if state == False:
            create_gtk4_user_override(self, self.settings)
        else:
            remove_gtk4_user_override(self, self.settings)

            buglog(f"user-flatpak-theming: {self.settings.get_boolean('user-flatpak-theming')}")

    # Placeholder function
    def on_allow_flatpak_theming_global_toggled(self, *args):
        state = self.allow_flatpak_theming_global.props.state

        if state == False:
            pass
        else:
            pass

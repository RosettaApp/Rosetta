from gettext import gettext as _

from gi.repository import Gtk, Adw

import json


class BaseProvider:
    name = None
    slug = None
    version = "0.1.7"
    developer_name = "0xMRTT"
    developers = ["0xMRTT https://github.com/0xMRTT"]
    license_type = Gtk.License.GPL_3_0
    copyright = "© 2023 0xMRTT"

    def __init__(self, win, app, *args, **kwargs):
        self.win = win
        self.banner = win.banner
        self.bot_text_view = win.bot_text_view
        self.app = app
        self.chat = None
        self.update_response = app.update_response

    def ask(self, prompt):
        raise NotImplementedError()

    @property
    def require_api_key(self):
        raise NotImplementedError()

    def preferences(self, win):
        return self.no_preferences(win)

    def no_api_key(self, title=None):
        if title:
            self.win.banner.props.title = title
        else:
            self.win.banner.props.title = _(
                "No API key provided, you can provide one in settings"
            )
        self.win.banner.props.button_label = _("Open settings")
        self.win.banner.connect("button-clicked", self.app.on_preferences_action)
        self.win.banner.set_revealed(True)

    def no_connection(self):
        self.win.banner.props.title = _("No network connection")
        self.win.banner.props.button_label = ""
        self.win.banner.set_revealed(True)

    def hide_banner(self):
        self.win.banner.set_revealed(False)

    def about(self, *args, **kwargs):
        about = Adw.AboutWindow(
            transient_for=self.pref_win,
            application_name=self.name,
            developer_name=self.developer_name,
            developers=self.developers,
            license_type=self.license_type,
            version=self.version,
            copyright=self.copyright,
        )
        about.present()

    def no_preferences(self, win):
        self.pref_win = win

        self.expander = Adw.ExpanderRow()
        self.expander.props.title = self.name

        # about_button = Gtk.Button()
        # about_button.set_label("About")
        # about_button.connect("clicked", self.about)
        # about_button.set_valign(Gtk.Align.CENTER)
        # self.expander.add_action(about_button)  # TODO: in Adw 1.4, use add_suffix

        enabled = Gtk.Switch()
        enabled.set_active(self.slug in self.app.enabled_providers)
        enabled.connect("notify::active", self.on_enabled)
        enabled.set_valign(Gtk.Align.CENTER)

        self.expander.add_action(enabled)

        self.no_pref_row = Adw.ActionRow()
        self.no_pref_row.props.title = "No preferences available"
        self.expander.add_row(self.no_pref_row)

        return self.expander

    def save(self):
        return {}

    def load(self, data):
        raise NotImplementedError()

    def chunk(self, prompt, n=4000):
        if len(prompt) > n:
            print("Chuncking prompt")
            prompt = [(prompt[i : i + n]) for i in range(0, len(prompt), n)]
        return prompt

    def on_enabled(self, widget, *args):
        if widget.get_active():
            self.app.enabled_providers.append(self.slug)
        else:
            self.app.enabled_providers.remove(self.slug)
        self.app.load_dropdown()

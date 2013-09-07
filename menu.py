""" Stores functions for rendering menus with Urwid.
"""

import urwid
from collection import Collection

class MainMenu():
    def __init__(self, collections):
        self.collections = collections
        self.selected = None
        self.widget = urwid.Padding([], left = 2, right = 2)
        self.top = urwid.Overlay(self.widget,
            urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align = 'center', width = ('relative', 60),
            valign = 'middle', height = ('relative', 60),
            min_width = 20, min_height = 9)

        self.main()

    def run(self):
        """ Enter the menu system """
        urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')]).run()

    def exit(self, button):
        """ Exit the menu system """
        raise urwid.ExitMainLoop()

    # ----------------------------------------
    # Specific menu screens

    def main(self, button=None, data=None):
        menu = NavigationMenu('Spaced Repetition', None)
        menu.add_option('New Collection', self.new_collection)
        menu.add_option('Study Collection', self.study_collection)
        menu.add_option('Edit Collection', self.choose_collection,
            {'Forward': self.edit_collection, 'Back': self.main})
        menu.add_option('Exit', self.exit)

        self.widget.original_widget = urwid.Padding(menu)

    def choose_slide(self, button, collection):
        pass

    def choose_collection(self, button, callbacks):
        def do_choose_collection(button, collection):
            callbacks['Forward'](button, collection)

        menu = NavigationMenu('Choose a Collection', callbacks['Back'])
        for collection in self.collections:
            menu.add_option(collection.name, do_choose_collection, collection)

        self.widget.original_widget = urwid.Padding(menu)

    def study_collection(self, button):
        pass

    def new_collection(self, button, data=None):
        """ Render the menu for creating a new Collection """

        def do_new_collection(button, dialogue_menu):
            """ Create a new collection with the data from the
                'new_collection' menu.
            """

            fields = dialogue_menu.get_fields()
            collection = Collection(fields['Name'])
            self.collections.append(collection)

            self.main()

        # ----------------------------------------
        # Start of new_collection() code

        menu = DialogueMenu(
                'Choose a collection',
                do_new_collection,
                self.main)
        menu.add_field("Name")

        self.widget.original_widget = urwid.Padding(menu)
    
    def edit_collection(self, button, collection):
        """ Render the menu for editing a collection """

        def do_edit_collection(button, dialogue_menu):
            """ Modify the collection with the data entered in the menu. """

            fields = dialogue_menu.get_fields()

            if fields['Name']:
                collection.name = fields['Name']

            self.main()

        # ----------------------------------------
        # Start of edit_collection() code

        menu = DialogueMenu(
                "Edit " + collection.name + ". Leave blank any field which you do not want to change.",
                do_edit_collection,
                self.main)
        menu.add_field("Name")

        self.widget.original_widget = urwid.Padding(menu)

class NavigationMenu(urwid.WidgetWrap):
    def __init__(self, title, back):
        if back == None:
            self.head = [urwid.Text(title), urwid.Divider()]
        else:
            back_button = self._button("Back", back, self)
            self.head = [urwid.Text(title), urwid.Divider(), back_button]
        self.body = []
        self._update_widget()

    def add_option(self, label, callback, data=None):
        """ Add a navigation option to the menu """
        self.body.append(self._button(label, callback, data))
        self._update_widget()

    def _update_widget(self):
        # Recreates the display widget. This should be called whenenver
        # anything is added to head or body.
        self.widget = urwid.ListBox(urwid.SimpleFocusListWalker(
            self.head + self.body))
        super().__init__(self.widget)

    def _button(self, label, callback, data=None):
        # An easier way to create a good looking button
        button = urwid.Button(label, callback, data)
        return urwid.AttrMap(button, None, focus_map='reversed')

class DialogueMenu(urwid.WidgetWrap):
    def __init__(self, title, forward, back):
        ok = self._button("OK", forward, self)
        cancel = self._button("Cancel", back, self)
        self.head = [urwid.Text(title), urwid.Divider()]
        self.body = []
        self.foot = [ok, cancel]
        self._update_widget()

    def add_field(self, label):
        """ Add an Edit widget to the body """
        self.body.append(urwid.Edit(label))
        self._update_widget()

    def get_fields(self):
        """ Returns the contents of all the dialogue boxes in a dictionary
            with the form, {"label": "contents"}
        """

        fields = {}
        for widget in self.body:
            label = widget.caption
            contents = widget.get_edit_text()
            fields[label] = contents

        return fields

    def _update_widget(self):
        # Recreates the display widget. This should be called whenenver
        # anything is added to head, body, or foot.
        self.widget = urwid.ListBox(urwid.SimpleFocusListWalker(
            self.head + self.body + self.foot))
        super().__init__(self.widget)

    def _button(self, label, callback, data=None):
        # An easier way to create a good looking button
        button = urwid.Button(label, callback, data)
        return urwid.AttrMap(button, None, focus_map='reversed')

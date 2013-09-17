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
    # Helper functions
    # ----------------------------------------

    def _update_widget(self, new_widget):
        """ Recreates the display widget. This should be called at the end of
        menu display functions.
        """
        self.widget.original_widget = urwid.Padding(new_widget)

    def _button(self, label, callback, data=None):
        """ An easier way to create a good looking button. """
        button = urwid.Button(label, callback, data)
        return urwid.AttrMap(button, None, focus_map='reversed')

    def _edit(self, label):
        """ An easier way to create an edit widget. """
        return urwid.Edit(label)

    # ----------------------------------------
    # Functions for rendering menu screens
    # ----------------------------------------

    def main(self, button=None, data=None):
        menu = GenericMenu('Please select an option')
        menu.add_widget(self._button('New Collection', self.new_collection))
        menu.add_widget(self._button('Study Collection', self.study_collection))
        menu.add_widget(self._button('Edit Collection', self.edit_collection))
        menu.add_widget(self._button('Exit', self.exit))

        self._update_widget(menu)

    def choose_slide(self, button, collection, forward=None, back=None):
        """ Render the menu for choosing a slide from a collection. """
        if forward == None:
            forward = self.edit_slide
        if back == None:
            back = self.main

        menu = GenericMenu('Choose a Slide')
        menu.add_widget(self._button("Back", back))
        for slide in collection.slides:
            menu.add_widget(self._button(slide.prompt, forward, slide))
        menu.add_widget(self._button("Back", back))

        self._update_widget(menu)

    def choose_collection(self, forward, back=None):
        """ Render the menu for choosing a collection from the list. """
        if back == None:
            back = self.main

        menu = GenericMenu('Choose a Collection')
        menu.add_widget(self._button("Back", back))
        for collection in self.collections:
            menu.add_widget(self._button(collection.name, forward, collection))
        menu.add_widget(self._button("Back", back))

        self._update_widget(menu)

    def study_collection(self, button):
        pass

    def new_collection(self, button, data=None):
        """ Render the menu for creating a new Collection """

        def do_new_collection(button, menu):
            """ Create a new collection with the data from the
                'new_collection' menu.
            """
            fields = menu.get_fields()
            collection = Collection(fields['Name'])
            self.collections.append(collection)

            self.main()
        # ----------------------------------------

        menu = DialogueMenu("Fill out the fields below to create a new collection.")
        menu.add_field("Name")
        menu.add_widget(self._button("Create Collection", do_new_collection, menu))

        self._update_widget(menu)
    
    def edit_collection(self, button, collection=None):
        """ Render the menu for editing a collection """

        def do_edit_collection(button, menu):
            """ Modify the collection with the data entered in the menu. """
            fields = menu.get_fields()

            if fields['Name']:
                collection.name = fields['Name']

            self.main()
        # ----------------------------------------

        if collection == None:
            self.choose_collection(self.edit_collection)
        else:
            menu = DialogueMenu("Edit " + collection.name + ". Leave blank any field which you do not want to change.")
            menu.add_field("Name")
            menu.add_widget(self._button("Edit Slides", self.choose_slide, collection))
            menu.add_widget(urwid.Divider('-'))
            menu.add_widget(self._button("Save", do_edit_collection, menu))
            menu.add_widget(self._button("Cancel", self.main))

            self._update_widget(menu)

    def edit_slide(self, button, slide):
        """ Render the menu for editing a slide in a collection """
        def do_edit_collection(button, menu):
            """ Modify the slide with the data entered in the menu. """
            fields = menu.get_fields()

            if fields['Prompt']:
                slide.prompt = fields['Prompt']
            if fields['Answer']:
                slide.answer = fields['Answer']

            self.main()
        # ----------------------------------------

        menu = DialogueMenu("Edit \"" + slide.prompt + "\". Leave blank any field which you do not want to change.")
        menu.add_field("Prompt")
        menu.add_field("Answer")
        menu.add_widget(urwid.Divider('-'))
        menu.add_widget(self._button("Save", do_edit_collection, menu))
        menu.add_widget(self._button("Cancel", self.main))

        self._update_widget(menu)

class GenericMenu(urwid.WidgetWrap):
    """ A bare-bones menu meant to encapsulate the most basic functions of a
    menu using Urwid. May be used to build more complex menus.
    """
    def __init__(self, title):
        self.head = [urwid.Text(title), urwid.Divider()]
        self.body = []
        self._update_widget()

    def add_widget(self, widget):
        """ Add a widget to the menu """
        self.body.append(widget)
        self._update_widget()

    def _update_widget(self):
        """ Recreates the display widget. This should be called whenenver
        anything is added to head or body.
        """
        self.widget = urwid.ListBox(urwid.SimpleFocusListWalker(
            self.head + self.body))
        super().__init__(self.widget)

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

class DialogueMenu(GenericMenu):
    """ A menu class which adds support for handing text fields. """
    def __init__(self, title):
        super().__init__(title)

    def add_field(self, label):
        """ Add an Edit widget to the body """
        self.add_widget(urwid.Edit(label))

    def get_fields(self):
        """ Returns the contents of all the dialogue boxes in a dictionary
            with the form, {"label": "contents"}
        """
        fields = {}
        for widget in self.body:
            # Try to get the label and contents of widgets. If it fails, the
            # widget probably isn't an edit widget, so there's no need to
            # worry about the exception.
            try:
                label = widget.caption
                contents = widget.get_edit_text()
                fields[label] = contents
            except:
                pass

        return fields

""" Stores functions for rendering menus with Urwid.
"""

import urwid
from collection import Collection

class Menu():
    def __init__(self, collections):
        self.collections = collections
        options = [
            ('New Collection', self.new_collection),
            ('Study Collection', self.choose_collection),
            ('Edit Collection', self.choose_collection),
            ('Exit', self.exit)]

        self.main = urwid.Padding(
            self.router_menu(u'Spaced Repetition', options),
            left = 2, right = 2)

        self.top = urwid.Overlay(self.main,
            urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align = 'center', width = ('relative', 60),
            valign = 'middle', height = ('relative', 60),
            min_width = 20, min_height = 9)

    def run(self):
        """ Runs the menu system """
        urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')]).run()

    def exit(self, button):
        """ Exits the menu system """
        raise urwid.ExitMainLoop()

    # ----------------------------------------
    # Specific menu screens

    def main_menu(self, button=None, data=None):
        options = [
            ('New Collection', self.new_collection),
            ('Study Collection', self.choose_collection),
            ('Edit Collection', self.choose_collection),
            ('Exit', self.exit)]

        self.main.original_widget = urwid.Padding(
            self.router_menu(u'Spaced Repetition', options))

    def item_chosen(self, button, choice):
        response = urwid.Text([u'You chose ', str(choice), u'\n'])
        done = urwid.Button(u'Ok')

        urwid.connect_signal(done, 'click', self.exit)
        self.main.original_widget = urwid.Filler(urwid.Pile([
            response, urwid.AttrMap(done, None, focus_map='reversed')]))

    def choose_slide(self, button, collection):
        self.main.original_widget = urwid.Padding(
            self.selection_menu(
                collection.name,
                collection.slides,
                self.item_chosen))

    def choose_collection(self, button):
        self.main.original_widget = urwid.Padding(
            self.selection_menu(
                'Choose a collection',
                self.collections,
                self.choose_slide))

    def new_collection(self, button):
        """ Render the menu for creating a new Collection """

        def do_new_collection(button, dialogue_menu):
            """ Create a new collection with the data from the
                'new_collection' menu.
            """

            fields = dialogue_menu.get_fields()
            collection = Collection(fields['Name'])
            self.collections.append(collection)

            self.edit_collection(None, collection)

        # ----------------------------------------
        # Start of new_collection() code

        menu = DialogueMenu(
                'Choose a collection',
                do_new_collection,
                self.main_menu)
        menu.add_field("Name")

        self.main.original_widget = urwid.Padding(menu)
    
    def edit_collection(self, button, collection):
        """ Render the menu for editing a collection """

        def do_edit_collection(button, dialogue_menu):
            """ Modify the collection with the data entered in the menu. """

            fields = dialogue_menu.get_fields()

            if fields['Name'] != "":
                collection.name = fields['Name']

            self.main_menu()

        # ----------------------------------------
        # Start of edit_collection() code

        menu = DialogueMenu(
                "Edit " + collection.name + ". Leave blank any field which you do not want to change.",
                do_edit_collection,
                self.main_menu)
        menu.add_field("Name")

        self.main.original_widget = urwid.Padding(menu)

    # ----------------------------------------
    # Constructors for menu structures

    def selection_menu(self, title, choices, callback, cancel=None):
        if not cancel:
            cancel = self.main_menu
        body = [urwid.Text(title), urwid.Divider()]

        button = urwid.Button('Cancel', cancel)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        for c in choices:
            button = urwid.Button(str(c), callback, c)

            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def router_menu(self, title, choices):
        body = [urwid.Text(title), urwid.Divider()]

        for c in choices:
            button = urwid.Button(str(c[0]), c[1])

            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

class DialogueMenu(urwid.WidgetWrap):
    def __init__(self, title, forward, back):
        ok = urwid.Button("OK", forward, self)
        cancel = urwid.Button("Cancel", back, self)
        self.head = [urwid.Text(title), urwid.Divider()]
        self.body = []
        self.foot = [ok, cancel]
        self._update_widget()

    def add_field(self, label):
        """ Adds an Edit widget to the body """
        widget = self._dialogue_box(label)

        #self.body.append(urwid.AttrMap(
            #widget, None, focus_map='reversed'))
        self.body.append(widget)
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

    def _dialogue_box(self, query):
        # Constructs a widget for a dialogue box.
        return urwid.Edit(query)

    def _update_widget(self):
        # Recreates the display widget. This should be called whenenver
        # anything is added to head, body, or foot.
        self.widget = urwid.ListBox(urwid.SimpleFocusListWalker(
            self.head + self.body + self.foot))
        super().__init__(self.widget)

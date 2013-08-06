""" Stores functions for rendering menus with Urwid.
"""

import urwid

class Menu():
    def __init__(self, collections):
        self.collections = collections
        self.main = urwid.Padding(
            self.selection_menu(u'Spaced Repetition', collections, self.choose_slide),
            left = 2, right = 2)

        self.top = urwid.Overlay(self.main,
            urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align = 'center', width = ('relative', 60),
            valign = 'middle', height = ('relative', 60),
            min_width = 20, min_height = 9)

    def run(self):
        urwid.MainLoop(self.top, palette=[('reversed', 'standout', '')]).run()

    def exit_program(self, button):
        raise urwid.ExitMainLoop()

    # ----------------------------------------
    # Specific menu screens

    def item_chosen(self, button, choice):
        response = urwid.Text([u'You chose ', str(choice), u'\n'])
        done = urwid.Button(u'Ok')

        urwid.connect_signal(done, 'click', self.exit_program)
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

    # ----------------------------------------
    # Constructors for menu structures

    def selection_menu(self, title, choices, callback):
        body = [urwid.Text(title), urwid.Divider()]

        for c in choices:
            button = urwid.Button(str(c))

            urwid.connect_signal(button, 'click', callback, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

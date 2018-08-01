#-*- coding:utf-8 -*-
#
# Copyright (C) 2018 sthoo <sth201807@gmail.com>
#
# Support: Report an issue at https://github.com/sth2018/FastWordQuery/issues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version; http://www.gnu.org/copyleft/gpl.html.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from aqt import mw
from aqt.qt import *
from anki.hooks import addHook, wrap
from aqt.addcards import AddCards
from aqt.utils import showInfo, shortcut
from .gui import show_options, show_about_dialog, check_updates
from .query import query_from_browser, query_from_editor_all_fields
from .context import config, APP_ICON
from .lang import _


__all__ = [
    'add_query_button', 'browser_menu', 
    'customize_addcards', 'config_menu', 
    'check_updates'
]


have_setup = False
my_shortcut = ''


def wrap_method(func, *args, **kwargs):
    '''
    wrap a function with params when it's called
    '''
    def callback():
        return func(*args, **kwargs)
    return callback


def add_query_button(self):
    '''
    add a button in add card window
    '''
    bb = self.form.buttonBox
    ar = QDialogButtonBox.ActionRole
    self.queryButton = bb.addButton(_(u"Query"), ar)
    self.queryButton.clicked.connect(wrap_method(
        query_from_editor_all_fields, self.editor))
    self.queryButton.setShortcut(QKeySequence(my_shortcut))
    self.queryButton.setToolTip(
        shortcut(_(u"Query (shortcut: %s)" % my_shortcut)))


def browser_menu():
    """
    add add-on's menu to browser window
    """
    def on_setup_menus(browser):
        """
        on browser setupMenus was called
        """
        # main menu
        menu = QMenu("FastWQ", browser.form.menubar)
        browser.form.menubar.addMenu(menu)
        # Query Selected
        action = QAction("Query Selected", browser)
        action.triggered.connect(wrap_method(query_from_browser, browser))
        action.setShortcut(QKeySequence(my_shortcut))
        menu.addAction(action)
        # Options
        action = QAction("Options", browser)
        def _show_options():
            model_id = -1
            for note_id in browser.selectedNotes():
                note = browser.mw.col.getNote(note_id)
                model_id = note.model()['id']
                break
            show_options(browser, model_id)
        action.triggered.connect(_show_options)
        menu.addAction(action)
        # About
        action = QAction("About", browser)
        action.triggered.connect(wrap_method(show_about_dialog, browser))
        menu.addAction(action)

    addHook('browser.setupMenus', on_setup_menus)


def customize_addcards():
    """
    add button to addcards window
    """
    AddCards.setupButtons = wrap(
        AddCards.setupButtons, add_query_button, "before")


def config_menu():
    """
    add menu to anki window menebar
    """
    action = QAction(APP_ICON, "FastWQ...", mw)
    action.triggered.connect(wrap_method(show_options))
    mw.form.menuTools.addAction(action)
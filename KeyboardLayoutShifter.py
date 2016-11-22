#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')

import gtk
import gnomeapplet
import gobject

import gconf

import sys
import codecs
import random

class KeyboardLayoutShifter(gnomeapplet.Applet):
    
    layoutkey = "/desktop/gnome/peripherals/keyboard/kbd/layouts"
    
    def getLayout(self):
        client = gconf.client_get_default()
        
        layoutentry = client.get(self.layoutkey)
        layoutentrylist = list(layoutentry.get_list())
        layout = layoutentrylist[0].get_string()
        return layout
    
    
    #Displays the next word to GUI. Uses set_markup to use HTML
    def shiftLayouts(self,bla=None):
        client = gconf.client_get_default()
        layoutentry = client.get(self.layoutkey)
        layoutentrylist = list(layoutentry.get_list())
        layoutentrylistshift = layoutentrylist[1:] + layoutentrylist[:1]
        layoutentry.set_list(layoutentrylistshift)
        client.set(self.layoutkey, layoutentry)
        
        layout = self.getLayout()
        layout = layout.replace('\t', ' ')
        self.hbut.set_label(layout)
        return True

    def __init__(self,applet,iid):
        self.applet = applet

        layout = self.getLayout()
        
        self.cont = gtk.HBox()
        
        
        self.hbut = gtk.Button(layout)
        self.hbut.connect("clicked", self.shiftLayouts)
        
        self.label = gtk.Label("HB")
        
        #self.applet.add(self.hbut)
        #self.applet.add(self.hbut)
        self.cont.add(self.label)
        self.cont.add(self.hbut)
        self.applet.add(self.cont)

        self.applet.show_all()
        #gobject.timeout_add(self.timeout_interval, self.displayNextWord)

#Register the applet datatype
gobject.type_register(KeyboardLayoutShifter)

def KeyboardLayoutShifter_factory(applet,iid):
    KeyboardLayoutShifter(applet,iid)
    return gtk.TRUE

#Very useful if I want to debug. To run in debug mode python hindiScroller.py -d
if len(sys.argv) == 2:
    if sys.argv[1] == "-d": #Debug mode
        main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        main_window.set_title("Python Applet")
        main_window.connect("destroy", gtk.main_quit)
        app = gnomeapplet.Applet()
        KeyboardLayoutShifter_factory(app,None)
        app.reparent(main_window)
        main_window.show_all()
        gtk.main()
        sys.exit()

#If called via gnome panel, run it in the proper way
if __name__ == '__main__':
    gnomeapplet.bonobo_factory("OAFIID:GNOME_KeyboardLayoutShifter_Factory", KeyboardLayoutShifter.__gtype__, "hello", "0", KeyboardLayoutShifter_factory)

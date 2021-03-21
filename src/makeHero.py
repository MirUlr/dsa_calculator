# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 21:51:11 2021

@author: Voovo
"""
from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys, os
from hero import Hero
from functools import partial
import numpy as np
from PyQt5 import QtCore

def loadHero():
    global charakter
    try: # Testen, ob als Held ladbar
        name = win.txt_heldName.text()
        ret = Hero.load(name,r'.\\')
    except ValueError: # nicht bekannt
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Dieser Held ist hier nicht bekannt.")
        msg.exec_()
    else: # es ist ein gültiger Held!
        charakter = ret
        # Eigenschaftswerte eintragen
        cnt = 0
        for key in charakter._attributes:
            funcName = 'e%i' % cnt
            method_to_call = getattr(win, funcName)
            method_to_call.setValue(charakter._attributes[key])
            cnt = cnt+1

        # Fertigkeitenwerte eintragen
        cnt = 0
        for key in charakter._skills:
            funcName = 'f%i' % cnt
            method_to_call = getattr(win, funcName)
            method_to_call.setValue(charakter._skills[key])
            cnt = cnt+1

        msg = QMessageBox()
        msg.setWindowTitle("Erfolg")
        msg.setText("Held erfolgreich geladen.")
        msg.exec_()

def saveHero():
    if win.txt_heldName.text() == "":
        name = "Mary Sue"
    else:
        name = win.txt_heldName.text()

    e =[]
    f =[]

    # Eigenschaftswerte
    for x in range(8):
        funcName = 'e%i' % x
        method_to_call = getattr(win, funcName)
        val = method_to_call.value()
        e.append(val)

    # Fertigkeitenwerte
    for x in range(59):
        funcName = 'f%i' % x
        method_to_call = getattr(win, funcName)
        val = method_to_call.value()
        f.append(val)

    charakter = Hero(name, e, f)

    if(isinstance(charakter, Hero)):
        charakter.save(r'.\\')
        msg = QMessageBox()
        msg.setWindowTitle("Erfolg")
        msg.setText("Held erfolgreich gespeichert!")
        msg.exec_()

if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setStyle("Fusion")

    # Fenster aus Designer laden
    win = uic.loadUi("makeHero.ui")

    win.btn_speichern.clicked.connect(saveHero)
    win.btn_laden.clicked.connect(loadHero)
    win.txt_heldName.returnPressed.connect(loadHero)

    # Fenster anzeigen
    win.show()
    sys.exit(app.exec_())

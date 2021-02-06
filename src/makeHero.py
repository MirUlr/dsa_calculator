# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 21:51:11 2021

@author: Voovo
"""
from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys, os
from held import Held
from functools import partial
import numpy as np
from PyQt5 import QtCore

def loadHero():
    global Charakter
    try: # Testen, ob als Held ladbar
        name = win.txt_heldName.text()
        ret = Held.laden(name,r'.\\')
    except ValueError: # nicht bekannt
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Dieser Held ist hier nicht bekannt.")
        msg.exec_()
    else: # es ist ein gültiger Held!
        Charakter = ret
        # Eigenschaftswerte eintragen
        cnt = 0
        for key in Charakter._eigenschaften:
            funcName = 'e%i' % cnt
            method_to_call = getattr(win, funcName)
            method_to_call.setValue(Charakter._eigenschaften[key])
            cnt = cnt+1

        # Fertigkeitenwerte eintragen
        cnt = 0
        for key in Charakter._fertigkeiten:
            funcName = 'f%i' % cnt
            method_to_call = getattr(win, funcName)
            method_to_call.setValue(Charakter._fertigkeiten[key])
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


    Charakter = Held(name, e, f)

    if(type(Charakter) == Held):
        Charakter.speichern(r'.\\')
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

    # Fenster anzeigen
    win.show()
    sys.exit(app.exec_())

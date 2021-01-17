# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 22:06:41 2021

@author: Voovo
"""
from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
import held
from functools import partial

# Fertigkeiten Funktion
def do(action, modi):
    result = Held.absolviere(action, modi())
    show(result)

# Würfelergebnis anzeigen
def show(result):
    win.label_result.setText("Ergebnis")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Fenster aus Designer laden
    win = uic.loadUi("MainWindow.ui")

    # Held initialisieren
    Held = held.Held.laden("Tore_Bjornson",r'D:\Voovo\Documents\RPG\DSA')

    # Button-Logik
    # ========================================================================
    # Fertigkeiten
    # ------------------------------------------------------------------------
    func_btn_fliegen = partial(do, "Fliegen",win.mod_fliegen.value)
    win.btn_fliegen.clicked.connect(func_btn_fliegen)


   # ========================================================================

   # Fenster anzeigen
    win.show()
    sys.exit(app.exec_())

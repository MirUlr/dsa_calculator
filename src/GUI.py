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

# Held laden
def load(name):
    global Held
    Held = held.Held.laden(name(),r'D:\Voovo\Documents\RPG\DSA')

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
    # Held laden
    func_btn_heldLaden = partial(load, win.txt_heldLaden.text)
    win.btn_heldLaden.clicked.connect(func_btn_heldLaden)

    # ========================================================================
    # Fertigkeiten
    # ------------------------------------------------------------------------
    # Körperfertigkeiten
    func_btn_fliegen = partial(do, "Fliegen",win.mod_fliegen.value)
    win.btn_fliegen.clicked.connect(func_btn_fliegen)

    func_btn_gaukeleien = partial(do, "Gaukeleien",win.mod_gaukeleien.value)
    win.btn_gaukeleien.clicked.connect(func_btn_gaukeleien)

    func_btn_klettern = partial(do, "Klettern",win.mod_klettern.value)
    win.btn_klettern.clicked.connect(func_btn_klettern)

    func_btn_koerperbeherrschung = partial(do, "Körperbeherrschung",win.mod_koerperbeherrschung.value)
    win.btn_koerperbeherrschung.clicked.connect(func_btn_koerperbeherrschung)

   # ========================================================================

   # Fenster anzeigen
    win.show()
    sys.exit(app.exec_())

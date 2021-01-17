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

    if(type(Held) == held.Held):
        win.tab_fertigkeiten.setEnabled(True)
        win.box_attribute.setEnabled(True)

# Fertigkeiten Funktion
def do(action, modi):
    result = Held.absolviere(action, modi())
    show(result)

# Würfelergebnis anzeigen
def show(result):
    win.label_result.setText(result)

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
    # Körpertalente
    func_btn_fliegen = partial(do, "Fliegen",win.mod_fliegen.value)
    win.btn_fliegen.clicked.connect(func_btn_fliegen)

    func_btn_gaukeleien = partial(do, "Gaukeleien",win.mod_gaukeleien.value)
    win.btn_gaukeleien.clicked.connect(func_btn_gaukeleien)

    func_btn_klettern = partial(do, "Klettern",win.mod_klettern.value)
    win.btn_klettern.clicked.connect(func_btn_klettern)

    func_btn_koerperbeherrschung = partial(do, "Körperbeherrschung",win.mod_koerperbeherrschung.value)
    win.btn_koerperbeherrschung.clicked.connect(func_btn_koerperbeherrschung)

    func_btn_kraftakt = partial(do, "Kraftakt",win.mod_kraftakt.value)
    win.btn_kraftakt.clicked.connect(func_btn_kraftakt)

    func_btn_reiten = partial(do, "Reiten",win.mod_reiten.value)
    win.btn_reiten.clicked.connect(func_btn_reiten)

    func_btn_schwimmen = partial(do, "Schwimmen",win.mod_schwimmen.value)
    win.btn_schwimmen.clicked.connect(func_btn_schwimmen)

    func_btn_selbstbeherrschung = partial(do, "Selbstbeherrschung",win.mod_selbstbeherrschung.value)
    win.btn_selbstbeherrschung.clicked.connect(func_btn_selbstbeherrschung)

    func_btn_singen = partial(do, "Singen",win.mod_singen.value)
    win.btn_singen.clicked.connect(func_btn_singen)

    func_btn_sinnesschaerfe = partial(do, "Sinnesschärfe",win.mod_sinnesschaerfe.value)
    win.btn_sinnesschaerfe.clicked.connect(func_btn_sinnesschaerfe)

    func_btn_tanzen = partial(do, "Tanzen",win.mod_tanzen.value)
    win.btn_tanzen.clicked.connect(func_btn_tanzen)

    func_btn_taschendiebstahl = partial(do, "Taschendiebstahl",win.mod_taschendiebstahl.value)
    win.btn_taschendiebstahl.clicked.connect(func_btn_taschendiebstahl)

    func_btn_verbergen = partial(do, "Verbergen",win.mod_verbergen.value)
    win.btn_verbergen.clicked.connect(func_btn_verbergen)

    func_btn_zechen = partial(do, "Zechen",win.mod_zechen.value)
    win.btn_zechen.clicked.connect(func_btn_zechen)

    # ------------------------------------------------------------------------
    # Gesellschaftstalente
    func_btn_bekehren = partial(do, "Bekehren & Überzeugen",win.mod_bekehren.value)
    win.btn_bekehren.clicked.connect(func_btn_bekehren)

    func_btn_betoeren = partial(do, "Betören",win.mod_betoeren.value)
    win.btn_betoeren.clicked.connect(func_btn_betoeren)

    func_btn_einschuechtern = partial(do, "Einschüchtern",win.mod_einschuechtern.value)
    win.btn_einschuechtern.clicked.connect(func_btn_einschuechtern)

    func_btn_etikette = partial(do, "Etikette",win.mod_etikette.value)
    win.btn_etikette.clicked.connect(func_btn_etikette)

    func_btn_gassenwissen = partial(do, "Gassenwissen",win.mod_gassenwissen.value)
    win.btn_gassenwissen.clicked.connect(func_btn_gassenwissen)

    func_btn_menschenkenntnis = partial(do, "Menschenkenntnis",win.mod_menschenkenntnis.value)
    win.btn_menschenkenntnis.clicked.connect(func_btn_menschenkenntnis)

    func_btn_ueberreden = partial(do, "Überreden",win.mod_ueberreden.value)
    win.btn_ueberreden.clicked.connect(func_btn_ueberreden)

    func_btn_verkleiden = partial(do, "Verkleiden",win.mod_verkleiden.value)
    win.btn_verkleiden.clicked.connect(func_btn_verkleiden)

    func_btn_willenskraft = partial(do, "Willenskraft",win.mod_willenskraft.value)
    win.btn_willenskraft.clicked.connect(func_btn_willenskraft)


   # ========================================================================

   # Fenster anzeigen
    win.show()
    sys.exit(app.exec_())

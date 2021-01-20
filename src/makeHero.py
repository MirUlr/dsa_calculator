# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 21:51:11 2021

@author: Voovo
"""
from PyQt5 import uic
from PyQt5.QtWidgets import *
import sys
import held
from functools import partial
import numpy as np


def saveHero():
    if win.txt_heldName.text() == "":
        name = "Mary Sue"
    else:
        name = win.txt_heldName.text()

    e =[]
    f =[]

    # Eigenschaften auslesen
    # ========================================================================
    e.append(win.mod_mut.value())
    e.append(win.mod_klugheit.value())
    e.append(win.mod_intuition.value())
    e.append(win.mod_charisma.value())
    e.append(win.mod_fingerfertigkeit.value())
    e.append(win.mod_gewandtheit.value())
    e.append(win.mod_konstitution.value())
    e.append(win.mod_koerperkraft.value())

    # Fertigkeiten auslesen
    # ========================================================================
    f.append(win.mod_fliegen.value())
    f.append(win.mod_gaukeleien.value())
    f.append(win.mod_klettern.value())
    f.append(win.mod_koerperbeherrschung.value())
    f.append(win.mod_kraftakt.value())
    f.append(win.mod_reiten.value())
    f.append(win.mod_schwimmen.value())
    f.append(win.mod_selbstbeherrschung.value())
    f.append(win.mod_singen.value())
    f.append(win.mod_sinnesschaerfe.value())
    f.append(win.mod_tanzen.value())
    f.append(win.mod_taschendiebstahl.value())
    f.append(win.mod_verbergen.value())
    f.append(win.mod_zechen.value())
    f.append(win.mod_bekehren.value())
    f.append(win.mod_betoeren.value())
    f.append(win.mod_einschuechtern.value())
    f.append(win.mod_etikette.value())
    f.append(win.mod_gassenwissen.value())
    f.append(win.mod_menschenkenntnis.value())
    f.append(win.mod_ueberreden.value())
    f.append(win.mod_verkleiden.value())
    f.append(win.mod_willenskraft.value())
    f.append(win.mod_faehrtensuche.value())
    f.append(win.mod_fesseln.value())
    f.append(win.mod_angeln.value())
    f.append(win.mod_orientierung.value())
    f.append(win.mod_pflanzenkunde.value())
    f.append(win.mod_tierkunde.value())
    f.append(win.mod_wildnisleben.value())
    f.append(win.mod_brettspiel.value())
    f.append(win.mod_geographie.value())
    f.append(win.mod_geschichtswissen.value())
    f.append(win.mod_kulte.value())
    f.append(win.mod_kriegskunst.value())
    f.append(win.mod_magiekunde.value())
    f.append(win.mod_mechanik.value())
    f.append(win.mod_rechnen.value())
    f.append(win.mod_rechtskunde.value())
    f.append(win.mod_sagen.value())
    f.append(win.mod_sphaerenkunde.value())
    f.append(win.mod_sternkunde.value())
    f.append(win.mod_alchemie.value())
    f.append(win.mod_boote.value())
    f.append(win.mod_fahrzeuge.value())
    f.append(win.mod_handel.value())
    f.append(win.mod_heilenGift.value())
    f.append(win.mod_heilenKrankheit.value())
    f.append(win.mod_heilenSeele.value())
    f.append(win.mod_heilenWunden.value())
    f.append(win.mod_holzbearbeitung.value())
    f.append(win.mod_lebensmittelbearbeitung.value())
    f.append(win.mod_lederbearbeitung.value())
    f.append(win.mod_malen.value())
    f.append(win.mod_metallbearbeitung.value())
    f.append(win.mod_musizieren.value())
    f.append(win.mod_schloesserknacken.value())
    f.append(win.mod_steinbearbeitung.value())
    f.append(win.mod_stoffbearbeitung.value())

    myHero = held.Held(name, e, f)

    if(type(myHero) == held.Held):
        myHero.speichern(r'.\\')
        msg = QMessageBox()
        msg.setWindowTitle("Erfolg")
        msg.setText("Held erfolgreich gespeichert!")
        msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Fenster aus Designer laden
    win = uic.loadUi("makeHero.ui")

    win.btn_speichern.clicked.connect(saveHero)

    # Fenster anzeigen
    win.show()
    sys.exit(app.exec_())

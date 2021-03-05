# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 22:06:41 2021

@author: Rabea
"""
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys, os
from hero import Hero
from twinkle import Twinkle
from functools import partial

# Charakter laden
def load(name):
    global charakter
    try: # Testen, ob als Funzel ladbar
        ret = Twinkle.load(name(),r'.\\')
    except KeyError: # nope, keine Funzel
        try: # Testen, ob als Held ladbar
            ret = Hero.load(name(),r'.\\')
        except ValueError: # nope, auch kein Held
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Dieser Held ist hier nicht bekannt.")
            msg.exec_()
        else: # es ist ein Held!
            charakter = ret
            # entsprechende GUI-Teile aktivieren/deaktivieren
            win.tab_fertigkeiten.setEnabled(True)
            win.box_attribute.setEnabled(True)
            win.label_funzel.setEnabled(False)
            win.comboBox_funzel.setEnabled(False)
            win.btn_funzel.setEnabled(False)
            win.mod_funzel.setEnabled(False)
            # clear ComboBox funzel
            win.comboBox_funzel.clear()

            # Eigenschaftswerte eintragen
            cnt = 0
            for key in charakter._eigenschaften:
                funcName = 'e%i' % cnt
                method_to_call = getattr(win, funcName)
                method_to_call.setText("  "+str(charakter._eigenschaften[key]))
                cnt = cnt+1

            # Fertigkeitenwerte eintragen
            cnt = 0
            for key in charakter._fertigkeiten:
                funcName = 'f%i' % cnt
                method_to_call = getattr(win, funcName)
                method_to_call.setText(str(charakter._fertigkeiten[key]))
                cnt = cnt+1

            msg = QMessageBox()
            msg.setWindowTitle("Erfolg")
            msg.setText("Held erfolgreich geladen.\nAuf ins Abenteuer!")
            msg.exec_()

    except ValueError: # unbekannter Dateiname
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Dieser Held ist hier nicht bekannt.")
            msg.exec_()
    else: # es ist eine Funzel!
        charakter = ret
        # clear ComboBox funzel
        win.comboBox_funzel.clear()
        # entsprechende GUI-Teile aktivieren
        win.tab_fertigkeiten.setEnabled(True)
        win.box_attribute.setEnabled(True)
        win.label_funzel.setEnabled(True)
        win.comboBox_funzel.setEnabled(True)
        win.btn_funzel.setEnabled(True)
        win.mod_funzel.setEnabled(True)

        # Dropdown-Menue der Funzel füllen
        for key in charakter._twinkle_stuff["Proben"]:
            win.comboBox_funzel.addItem(key)


        # Eigenschaftswerte eintragen
        cnt = 0
        for key in charakter._eigenschaften:
            funcName = 'e%i' % cnt
            method_to_call = getattr(win, funcName)
            method_to_call.setText("  "+str(charakter._eigenschaften[key]))
            cnt = cnt+1

        # Fertigkeitenwerte eintragen
        cnt = 0
        for key in charakter._fertigkeiten:
            funcName = 'f%i' % cnt
            method_to_call = getattr(win, funcName)
            method_to_call.setText(str(charakter._fertigkeiten[key]))
            cnt = cnt+1

        msg = QMessageBox()
        msg.setWindowTitle("Erfolg")
        msg.setText("Funzel erfolgreich geladen.\nAuf ins Abenteuer!")
        msg.exec_()

# Fertigkeiten Funktion
def do(action, modi):
    result = charakter.execute(action, modi())
    show(result)

# Fertigkeiten Funktion
def do_funzel(action, modi):
    result = charakter.perform(action(), modi())
    show(result)

# Eigenschaften Funktion
def test(action, modi):
    result = charakter.test(action, modi())
    show(result)

# Würfelergebnis anzeigen
def show(result):
    win.label_result.setText(result)

if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app.setStyle("Fusion")

    # Fenster aus Designer laden
    win = uic.loadUi("MainWindow.ui")

    # charakter initialisieren, zum Testen
    # charakter = Hero.load("Tore_Bjornson",r'D:\Voovo\Documents\RPG\DSA')

    # Button-Logik
    # ========================================================================
    # Charakter laden
    func_btn_heldLaden = partial(load, win.txt_heldLaden.text)
    win.btn_heldLaden.clicked.connect(func_btn_heldLaden)

    # ========================================================================
    # Eigenschaften
    func_btn_mut = partial(test, "Mut",win.mod_mut.value)
    win.btn_mut.clicked.connect(func_btn_mut)

    func_btn_klugheit = partial(test, "Klugheit",win.mod_klugheit.value)
    win.btn_klugheit.clicked.connect(func_btn_klugheit)

    func_btn_intuition = partial(test, "Intuition",win.mod_intuition.value)
    win.btn_intuition.clicked.connect(func_btn_intuition)

    func_btn_charisma = partial(test, "Charisma",win.mod_charisma.value)
    win.btn_charisma.clicked.connect(func_btn_charisma)

    func_btn_fingerfertigkeit = partial(test, "Fingerfertigkeit",win.mod_fingerfertigkeit.value)
    win.btn_fingerfertigkeit.clicked.connect(func_btn_fingerfertigkeit)

    func_btn_gewandtheit = partial(test, "Gewandtheit",win.mod_gewandtheit.value)
    win.btn_gewandtheit.clicked.connect(func_btn_gewandtheit)

    func_btn_konstitution = partial(test, "Konstitution",win.mod_konstitution.value)
    win.btn_konstitution.clicked.connect(func_btn_konstitution)

    func_btn_koerperkraft = partial(test, "Körperkraft",win.mod_koerperkraft.value)
    win.btn_koerperkraft.clicked.connect(func_btn_koerperkraft)

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

    # ------------------------------------------------------------------------
    # Naturtalente
    func_btn_faehrtensuche = partial(do, "Fährtensuchen",win.mod_faehrtensuche.value)
    win.btn_faehrtensuche.clicked.connect(func_btn_faehrtensuche)

    func_btn_fesseln = partial(do, "Fesseln",win.mod_fesseln.value)
    win.btn_fesseln.clicked.connect(func_btn_fesseln)

    func_btn_angeln = partial(do, "Fischen & Angeln",win.mod_angeln.value)
    win.btn_angeln.clicked.connect(func_btn_angeln)

    func_btn_orientierung = partial(do, "Orientierung",win.mod_orientierung.value)
    win.btn_orientierung.clicked.connect(func_btn_orientierung)

    func_btn_pflanzenkunde = partial(do, "Pflanzenkunde",win.mod_pflanzenkunde.value)
    win.btn_pflanzenkunde.clicked.connect(func_btn_pflanzenkunde)

    func_btn_tierkunde = partial(do, "Tierkunde",win.mod_tierkunde.value)
    win.btn_tierkunde.clicked.connect(func_btn_tierkunde)

    func_btn_wildnisleben = partial(do, "Wildnisleben",win.mod_wildnisleben.value)
    win.btn_wildnisleben.clicked.connect(func_btn_wildnisleben)

    # ------------------------------------------------------------------------
    # Wissenstalente
    func_btn_brettspiel = partial(do, "Brett- & Glücksspiel",win.mod_brettspiel.value)
    win.btn_brettspiel.clicked.connect(func_btn_brettspiel)

    func_btn_geographie = partial(do, "Geographie",win.mod_geographie.value)
    win.btn_geographie.clicked.connect(func_btn_geographie)

    func_btn_geschichtswissen = partial(do, "Geschichtswissen",win.mod_geschichtswissen.value)
    win.btn_geschichtswissen.clicked.connect(func_btn_geschichtswissen)

    func_btn_kulte = partial(do, "Götter & Kulte",win.mod_kulte.value)
    win.btn_kulte.clicked.connect(func_btn_kulte)

    func_btn_kriegskunst = partial(do, "Kriegskunst",win.mod_kriegskunst.value)
    win.btn_kriegskunst.clicked.connect(func_btn_kriegskunst)

    func_btn_magiekunde = partial(do, "Magiekunde",win.mod_magiekunde.value)
    win.btn_magiekunde.clicked.connect(func_btn_magiekunde)

    func_btn_mechanik = partial(do, "Mechanik",win.mod_mechanik.value)
    win.btn_mechanik.clicked.connect(func_btn_mechanik)

    func_btn_rechnen = partial(do, "Rechnen",win.mod_rechnen.value)
    win.btn_rechnen.clicked.connect(func_btn_rechnen)

    func_btn_rechtskunde = partial(do, "Rechtskunde",win.mod_rechtskunde.value)
    win.btn_rechtskunde.clicked.connect(func_btn_rechtskunde)

    func_btn_sagen = partial(do, "Sagen & Legenden",win.mod_sagen.value)
    win.btn_sagen.clicked.connect(func_btn_sagen)

    func_btn_sphaerenkunde = partial(do, "Sphärenkunde",win.mod_sphaerenkunde.value)
    win.btn_sphaerenkunde.clicked.connect(func_btn_sphaerenkunde)

    func_btn_sternkunde = partial(do, "Sternkunde",win.mod_sternkunde.value)
    win.btn_sternkunde.clicked.connect(func_btn_sternkunde)

    # ------------------------------------------------------------------------
    # Handwerkstalente
    func_btn_alchemie = partial(do, "Alchimie",win.mod_alchemie.value)
    win.btn_alchemie.clicked.connect(func_btn_alchemie)

    func_btn_boote = partial(do, "Boote & Schiffe",win.mod_boote.value)
    win.btn_boote.clicked.connect(func_btn_boote)

    func_btn_fahrzeuge = partial(do, "Fahrzeuge",win.mod_fahrzeuge.value)
    win.btn_fahrzeuge.clicked.connect(func_btn_fahrzeuge)

    func_btn_handel = partial(do, "Handel",win.mod_handel.value)
    win.btn_handel.clicked.connect(func_btn_handel)

    func_btn_heilenGift = partial(do, "Heilkunde Gift",win.mod_heilenGift.value)
    win.btn_heilenGift.clicked.connect(func_btn_heilenGift)

    func_btn_heilenKrankheit = partial(do, "Heilkunde Krankheiten",win.mod_heilenKrankheit.value)
    win.btn_heilenKrankheit.clicked.connect(func_btn_heilenKrankheit)

    func_btn_heilenSeele = partial(do, "Heilkunde Seele",win.mod_heilenSeele.value)
    win.btn_heilenSeele.clicked.connect(func_btn_heilenSeele)

    func_btn_heilenWunden = partial(do, "Heilkunde Wunden",win.mod_heilenWunden.value)
    win.btn_heilenWunden.clicked.connect(func_btn_heilenWunden)

    func_btn_holzbearbeitung = partial(do, "Holzbearbeitung",win.mod_holzbearbeitung.value)
    win.btn_holzbearbeitung.clicked.connect(func_btn_holzbearbeitung)

    func_btn_lebensmittelbearbeitung = partial(do, "Lebensmittelbearbeitung",win.mod_lebensmittelbearbeitung.value)
    win.btn_lebensmittelbearbeitung.clicked.connect(func_btn_lebensmittelbearbeitung)

    func_btn_lederbearbeitung = partial(do, "Lederbearbeitung",win.mod_lederbearbeitung.value)
    win.btn_lederbearbeitung.clicked.connect(func_btn_lederbearbeitung)

    func_btn_malen = partial(do, "Malen & Zeichen",win.mod_malen.value)
    win.btn_malen.clicked.connect(func_btn_malen)

    func_btn_metallbearbeitung = partial(do, "Metallbearbeitung",win.mod_metallbearbeitung.value)
    win.btn_metallbearbeitung.clicked.connect(func_btn_metallbearbeitung)

    func_btn_musizieren = partial(do, "Musizieren",win.mod_musizieren.value)
    win.btn_musizieren.clicked.connect(func_btn_musizieren)

    func_btn_schloesserknacken = partial(do, "Schlösserknacken",win.mod_schloesserknacken.value)
    win.btn_schloesserknacken.clicked.connect(func_btn_schloesserknacken)

    func_btn_steinbearbeitung = partial(do, "Steinbearbeitung",win.mod_steinbearbeitung.value)
    win.btn_steinbearbeitung.clicked.connect(func_btn_steinbearbeitung)

    func_btn_stoffbearbeitung = partial(do, "Stoffbearbeitung",win.mod_stoffbearbeitung.value)
    win.btn_stoffbearbeitung.clicked.connect(func_btn_stoffbearbeitung)

    # ------------------------------------------------------------------------
    # Funzelkram
    func_btn_funzel = partial(do_funzel, win.comboBox_funzel.currentText,win.mod_funzel.value)
    win.btn_funzel.clicked.connect(func_btn_funzel)


   # ========================================================================

   # Fenster anzeigen
    win.show()
    sys.exit(app.exec_())

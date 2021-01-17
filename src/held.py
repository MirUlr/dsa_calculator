# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 09:27:20 2021

@author: Mirko Ulrich
"""

import json
import pathlib

import numpy as np


class Held():
    FERTIGKEITSPROBEN = {
        'Fliegen': ('Mut', 'Intuition', 'Gewandtheit'),
        'Gaukeleien': ('Mut', 'Charisma', 'Fingerfertigkeit'),
        'Klettern': ('Mut', 'Gewandtheit', 'Körperkraft'),
        'Körperbeherrschung': ('Gewandtheit', 'Gewandtheit', 'Konstitution'),
        'Kraftakt': ('Konstitution', 'Körperkraft', 'Körperkraft'),
        'Reiten': ('Charisma', 'Gewandtheit', 'Körperkraft'),
        'Schwimmen': ('Gewandtheit', 'Konstitution', 'Körperkraft'),
        'Selbstbeherrschung': ('Mut', 'Mut', 'Konstitution'),
        'Singen': ('Klugheit', 'Charisma', 'Konstitution'),
        'Sinnesschärfe': ('Klugheit', 'Intuition', 'Intuition'),
        'Tanzen': ('Klugheit', 'Charisma', 'Gewandtheit'),
        'Taschendiebstahl': ('Mut', 'Fingerfertigkeit', 'Gewandtheit'),
        'Verbergen': ('Mut', 'Intuition', 'Gewandtheit'),
        'Zechen': ('Klugheit', 'Konstitution', 'Körperkraft'),
        'Bekehren & Überzeugen': ('Mut', 'Klugheit', 'Charisma'),
        'Betören': ('Mut', 'Charisma', 'Charisma'),
        'Einschüchtern': ('Mut', 'Intuition', 'Charisma'),
        'Etikette': ('Klugheit', 'Intuition', 'Charisma'),
        'Gassenwissen': ('Klugheit', 'Intuition', 'Charisma'),
        'Menschenkenntnis': ('Klugheit', 'Intuition', 'Charisma'),
        'Überreden': ('Mut', 'Intuition', 'Charisma'),
        'Verkleiden': ('Intuition', 'Charisma', 'Gewandtheit'),
        'Willenskraft': ('Mut', 'Intuition', 'Charisma'),
        'Fährtensuchen': ('Mut', 'Intuition', 'Gewandtheit'),
        'Fesseln': ('Klugheit', 'Fingerfertigkeit', 'Körperkraft'),
        'Fischen & Angeln': ('Fingerfertigkeit', 'Gewandtheit', 'Konstitution'),
        'Orientierung': ('Klugheit', 'Intuition', 'Intuition'),
        'Pflanzenkunde': ('Klugheit', 'Fingerfertigkeit', 'Konstitution'),
        'Tierkunde': ('Mut', 'Mut', 'Charisma'),
        'Wildnisleben': ('Mut', 'Gewandtheit', 'Konstitution'),
        'Brett- & Glücksspiel': ('Klugheit', 'Klugheit', 'Intuition'),
        'Geographie': ('Klugheit', 'Klugheit', 'Intuition'),
        'Geschichtswissen':  ('Klugheit', 'Klugheit', 'Intuition'),
        'Götter & Kulte': ('Klugheit', 'Klugheit', 'Intuition'),
        'Kriegskunst': ('Mut', 'Klugheit', 'Intuition'),
        'Magiekunde': ('Klugheit', 'Klugheit', 'Intuition'),
        'Mechanik': ('Klugheit', 'Klugheit', 'Fingerfertigkeit'),
        'Rechnen': ('Klugheit', 'Klugheit', 'Intuition'),
        'Rechtskunde': ('Klugheit', 'Klugheit', 'Intuition'),
        'Sagen & Legenden': ('Klugheit', 'Klugheit', 'Intuition'),
        'Sphärenkunde': ('Klugheit', 'Klugheit', 'Intuition'),
        'Sternkunde':  ('Klugheit', 'Klugheit', 'Intuition'),
        'Alchimie': ('Mut', 'Klugheit', 'Fingerfertigkeit'),
        'Boote & Schiffe': ('Fingerfertigkeit', 'Gewandtheit', 'Körperkraft'),
        'Fahrzeuge':  ('Charisma', 'Fingerfertigkeit', 'Konstitution'),
        'Handel':  ('Klugheit', 'Intuition', 'Charisma'),
        'Heilkunde Gift': ('Mut', 'Klugheit', 'Intuition'),
        'Heilkunde Krankheiten': ('Mut', 'Intuition', 'Konstitution'),
        'Heilkunde Seele': ('Intuition', 'Charisma', 'Konstitution'),
        'Heilkunde Wunden': ('Klugheit', 'Fingerfertigkeit',
                             'Fingerfertigkeit'),
        'Holzbearbeitung': ('Fingerfertigkeit', 'Gewandtheit', 'Körperkraft'),
        'Lebensmittelbearbeitung': ('Intuition', 'Fingerfertigkeit',
                                    'Fingerfertigkeit'),
        'Lederbearbeitung': ('Fingerfertigkeit', 'Gewandtheit', 'Konstitution'),
        'Malen & Zeichen': ('Intuition', 'Fingerfertigkeit',
                            'Fingerfertigkeit'),
        'Metallbearbeitung': ('Fingerfertigkeit', 'Konstitution',
                              'Körperkraft'),
        'Musizieren': ('Charisma', 'Fingerfertigkeit', 'Konstitution'),
        'Schlösserknacken': ('Intuition', 'Fingerfertigkeit',
                             'Fingerfertigkeit'),
        'Steinbearbeitung': ('Fingerfertigkeit', 'Fingerfertigkeit',
                             'Körperkraft'),
        'Stoffbearbeitung': ('Klugheit', 'Fingerfertigkeit',
                             'Fingerfertigkeit')
        }

    def __init__(self, name, eigenschaftswerte=[], fertigkeitenwerte=[]):
        self.name = name
        self._eigenschaften = dict.fromkeys(
            ['Mut', 'Klugheit', 'Intuition', 'Charisma', 'Fingerfertigkeit',
             'Gewandtheit', 'Konstitution', 'Körperkraft'])
        self.__fertigkeiten = dict.fromkeys(
            list(self.FERTIGKEITSPROBEN.keys()))

        if len(eigenschaftswerte) != len(self._eigenschaften):
            print('###  Nun Eigenschaften eingeben  ###')
            eigenschaftswerte = self.__ask_for_values(self._eigenschaften,
                                                      (1, 19))
        self._eigenschaften = {
            list(self._eigenschaften.keys())[i]: eigenschaftswerte[i]
            for i in range(len(eigenschaftswerte))}

        if len(fertigkeitenwerte) != len(self.__fertigkeiten):
            print('###  Nun Eigenschaften eingeben  ###')
            fertigkeitenwerte = self.__ask_for_values(self.__fertigkeiten,
                                                      (0, 25))
        self.__fertigkeiten = {
            list(self.__fertigkeiten.keys())[i]: fertigkeitenwerte[i]
            for i in range(len(fertigkeitenwerte))}

    @classmethod
    def _from_json(cls, name, stats):
        hero = cls(name,
                   list(stats['Eigenschaften'].values()),
                   list(stats['Fertigkeiten'].values()))
        return hero

    @classmethod
    def laden(cls, charakter='',
              verzeichnis='C:/Users/reMner/Desktop/PnP/DSA'):
        final_file = pathlib.Path(verzeichnis,
                                  (charakter + '.json').replace(' ', '_'))
        if final_file.exists() and final_file.is_file():
            with open(final_file, 'r') as source:
                data = json.load(source)
            return cls._from_json(name=charakter.replace('_', ' '),
                                  stats=data)
        else:
            print('Keine gültigen Daten gefunden.')

    def speichern(self, dateipfad='C:/Users/reMner/Desktop/PnP/DSA'):
        dateipfad = pathlib.Path(dateipfad)
        if dateipfad.exists() and dateipfad.is_dir():
            file = '{}.json'.format(self.name.replace(' ', '_'))
            data_to_dump = {'Eigenschaften': self._eigenschaften,
                            'Fertigkeiten': self.__fertigkeiten}
            with open(pathlib.Path(dateipfad, file),
                      'w') as file:
                json.dump(data_to_dump, file)
        else:
            print('Mit gültigem Pfad erneut versuchen.')

    def zeige_eigenschaften(self):
        self.__show_pretty_dicts('{}\'s Eigenschaften:'.format(self.name),
                                 self._eigenschaften)

    def zeige_fertigkeiten(self):
        self.__show_pretty_dicts('{}\'s Fertigkeiten:'.format(self.name),
                                 self.__fertigkeiten)

    def absolviere(self, talent, modifikator=-0):
        try:
            zielwerte = np.array(
                [self._eigenschaften[eig]
                 for eig in self.FERTIGKEITSPROBEN[talent]])
            add_cap_19 = np.vectorize(
                lambda x: min(19, x + modifikator)
                )
            zielwerte = add_cap_19(zielwerte)
        except KeyError:
            print('{} ist keine gültige Fertigkeit.'.format(talent))

        if any(zielwerte < 1):                  # unmögliche Proben detektieren
            print('Die Erschwernis von {} '
                  'macht diese Probe unmöglich.'.format(abs(modifikator)))
            return

        _3w20 = np.random.randint(1, 21, 3)

        ausgleich = _3w20 - zielwerte
        ausgleich[ausgleich < 0] = 0                # kein discount auf Erfolge
        übrig = self.__fertigkeiten[talent] - sum(ausgleich)

        # Bestimmen von Patzer und krit. Erfol
        würfel_p = _3w20.copy()
        würfel_p[würfel_p != 20] = 0
        patzer = sum(würfel_p) > 20       # <=> mehr als eine zwanzig gewürfelt

        würfel_k = _3w20.copy()
        würfel_k[würfel_k != 1] = 0
        krit = sum(würfel_k) > 1             # <=> mehr als eine eins gewürfelt

        if (übrig >= 0 and not patzer) or krit:
            gelungen = True
            qualitätsstufen = self.__determine_quality_level(übrig)
            if krit:
                qualitätsstufen *= 2
        else:
            gelungen = False

        # Teile die Ergebnisse der Welt mit!
        trenner = '='*75

        if modifikator == 0:
            probe = '{} absolviert eine Probe auf {}, Fertigkeitswert {}.'
        else:
            if modifikator < 0:
                probe = '{} absolviert eine um ' +\
                    str(abs(modifikator)) +\
                    ' erschwerte Probe auf {}, Fertigkeitswert {}.'
            else:
                probe = '{} absolviert eine um ' +\
                    str(abs(modifikator)) +\
                    ' erleichterte Probe auf {}, Fertigkeitswert {}.'

        zu_erzielen = 'Eigenschaften:\n\t{} {} {}\nZielwerte:\n\t{}'.format(
            *self.FERTIGKEITSPROBEN[talent], zielwerte)
        zufallsereignis = 'Würfelergebnis:\n\t{}\n'.format(_3w20)

        if gelungen:
            resultat = 'Ergebnis:\tErfolg mit {} Qualitätsstufe(n).'.format(
                qualitätsstufen)
            if krit:
                resultat += '\t=D'
        else:
            if patzer:
                resultat = 'Ergebnis:\tPatzer'
            else:
                resultat = 'Ergebnis:\tFehlschlag'

        # Ausgabe
        print(trenner)
        print(probe.format(self.name, talent, self.__fertigkeiten[talent]))
        print(zu_erzielen)
        print(zufallsereignis)
        print(resultat)

    @staticmethod
    def __ask_for_values(dictionary, limits=(-float('inf'), float('inf'))):
        values = []
        for key in dictionary.keys():
            clean_read = False
            while not clean_read:
                try:
                    val = int(input('Wert für {} eingeben:\t'.format(key)))
                    if val < limits[0] or limits[1] < val:
                        print(
                            'Wert muss sich in Bereich '
                            'von {} bis {} bewegen'.format(*limits),
                            end='\t')
                    else:
                        clean_read = True
                except ValueError:
                    print('Wert muss als Integer lesbar sein.', end='\t')
            values.append(val)
        return values

    @staticmethod
    def __show_pretty_dicts(title, dictionary, alphabetical_order=True):
        list_of_keys = list(dictionary.keys())
        if alphabetical_order:
            list_of_keys.sort()

        underline = '\n' + '=' * len(title)
        print('\n' + title + underline)
        for key in list_of_keys:
            print(key + ':\n\t' + str(dictionary[key]))

    @staticmethod
    def __determine_quality_level(spare_points):
        if 0 <= spare_points <= 3:
            quality_level = 1
        elif 4 <= spare_points <= 6:
            quality_level = 2
        elif 7 <= spare_points <= 9:
            quality_level = 3
        elif 10 <= spare_points <= 12:
            quality_level = 4
        elif 13 <= spare_points <= 15:
            quality_level = 5
        elif 16 <= spare_points:
            quality_level = 6
        else:
            quality_level = -1
        return quality_level

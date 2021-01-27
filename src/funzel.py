# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 17:26:37 2021

@author: Mirko Ulrich
"""

import json
import pathlib

import numpy as np

from held import Held


class Funzel(Held):

    def __init__(self, name, funzeligkeit,
                 eigenschaftswerte=[], fertigkeitenwerte=[],
                 unfähigkeiten=None, begabungen=None,
                 funzel_fertigkeiten={}):
        assert funzeligkeit in ['Geweihter', 'Geweihte',
                                'Hexer', 'Hexe', 'Zauberer', 'Zauberin'],\
            '{} ist keine unterstützte Rolle.'.format(funzeligkeit)
        super().__init__(name, eigenschaftswerte, fertigkeitenwerte,
                         unfähigkeiten, begabungen)
        self.rolle = funzeligkeit

        if len(funzel_fertigkeiten.keys()) == 0:
            self._funzelkram = self.__ask_for_funzel_stuff()
        else:
            self._funzelkram = funzel_fertigkeiten

    def __ask_for_funzel_stuff(self,
                               funzel_dict={'Proben': {},
                                            'Fertigkeitswerte': {}}):
        response = super()._clean_read(
            text='Sollen weitere {} aufgenommen werden?\n(j/n) '.format(
                self.__funzel_stuff_term(False)),
            legal_response=['j', 'n'])

        if response == 'j':                         # record more funzel stuff
            # Name des Zaubers oder Wirkung
            bezeichner = input('Name des/der {}: '.format(
                self.__funzel_stuff_term(True)))
            # die drei Eigenschaften für die Probe
            eig = []
            while len(eig) < 3:
                val = input('{}. Eigenschaft für {}: '.format(len(eig)+1,
                                                              bezeichner))
                if val in self._eigenschaften.keys():
                    eig.append(val)
                else:
                    print('{} ist keine gültige Eigenschaft.'.format(val))
            # Fertigkeitswert des Zaubers / der Wirkung
            clean_read = False
            while not clean_read:
                try:
                    fertigkeitswert = int(
                        input('Fertigkeitswert für {}: '.format(bezeichner))
                        )
                    if fertigkeitswert in range(0, 26):
                        clean_read = True
                    else:
                        print('Wert muss zwischen 0 und 25 liegen.')
                except ValueError:
                    print('Wert muss als Integer lesbar sein.')

            # Nachfrage, ob man sich sicher ist
            clean_read = False
            while not clean_read:
                response = input('{} mit Fertigkeitswert {} und Proben auf'
                                 ' {}, {} und {} hinzufügen?\n(j/n) '.format(
                                     bezeichner, fertigkeitswert, *eig))
                if response in ['j', 'n']:
                    clean_read = True
            if response == 'j':
                funzel_dict['Proben'][bezeichner] = tuple(eig)
                funzel_dict['Fertigkeitswerte'][bezeichner] = fertigkeitswert

            # rekursiv nach weitern Zaubern fragen
            return self.__ask_for_funzel_stuff(funzel_dict)
        else:
            return funzel_dict

    def __funzel_stuff_term(self, singular: bool):
        if self.rolle in ['Geweihte', 'Geweihter']:
            if singular:
                term = 'Liturgie/Zeremonie'
            else:
                term = 'Liturgien & Zeremonien'
        elif self.rolle in ['Zauberin', 'Zauberer']:
            if singular:
                term = 'Zauber/Ritual'
            else:
                term = 'Zauber & Rituale'
        elif self.rolle in ['Hexe', 'Hexer']:
            if singular:
                term = 'Hexerei'
            else:
                term = 'Hexereien'
        else:
            if singular:
                term = 'Funzelding'
            else:
                term = 'Funzeldinge'
        return term

    def speichern(self, dateipfad='C:/Users/reMner/Desktop/PnP/DSA'):
        dateipfad = pathlib.Path(dateipfad)
        if dateipfad.exists() and dateipfad.is_dir():
            file = '{}.json'.format(self.name.replace(' ', '_'))
            data_to_dump = {'Profession': self.rolle,
                            'Eigenschaften': self._eigenschaften,
                            'Fertigkeiten': self._fertigkeiten,
                            'Funzelfertigkeiten': self._funzelkram,
                            'Begabungen': list(self._begabungen),
                            'Unfähigkeiten': list(self._unfähigkeiten)}
            with open(pathlib.Path(dateipfad, file),
                      'w') as file:
                json.dump(data_to_dump, file)
        else:
            raise OSError('Mit gültigem Pfad erneut versuchen.'
                          ' Eventuell Schreibrechte überprüfen.')

    def zeige_übernatürliche_fähigkeiten(self):
        title = '{}\'s {}:'.format(self.name, self.__funzel_stuff_term(False))
        return super()._show_pretty_dicts(title, self._funzelkram)

    @classmethod
    def _from_json(cls, name, stats):
        try:
            incompetences = stats['Unfähigkeiten']
        except KeyError:
            incompetences = None

        try:
            gifted_talents = stats['Begabungen']
        except KeyError:
            gifted_talents = None

        hero = cls(name,
                   stats['Profession'],
                   list(stats['Eigenschaften'].values()),
                   list(stats['Fertigkeiten'].values()),
                   incompetences,
                   gifted_talents,
                   stats['Funzelfertigkeiten'])
        return hero

    def aktualisiere_besondere_befähigungen(self,
                                            weiterhin_zulässig=[]):
        super().aktualisiere_besondere_befähigungen(
            weiterhin_zulässig=list(self._funzelkram['Proben'].keys()))

    def durchführen(self, fähigkeit: str, modifikator=0):
        try:
            zielwerte = np.array(
                [self._eigenschaften[eig]
                 for eig in self._funzelkram['Proben'][fähigkeit]])
            add_cap_19 = np.vectorize(
                lambda x: min(19, x + modifikator)
                )
            zielwerte = add_cap_19(zielwerte)
        except KeyError:
            raise KeyError('{} ist kein(e) gültige(r) {}.'.format(
                fähigkeit, self.__funzel_stuff_term(singular=True)))

        if any(zielwerte < 1):                  # unmögliche Proben detektieren
            msg = ('Die Erschwernis von {} '
                   'macht diese Probe unmöglich.'.format(abs(modifikator)))
            return msg

        _3w20 = np.random.randint(1, 21, 3)

        # Zufallsereignis auswerten
        gelungen, krit, qualitätsstufen = self._perform_test(
            aim=zielwerte, random_event=_3w20,
            skill_level=self._funzelkram['Fertigkeitswerte'][fähigkeit],
            gifted=(fähigkeit in self._begabungen))

        # Ausgabe bestimmen
        out = self._format_outcome(
            skill=fähigkeit,
            goals=zielwerte,
            random_event=_3w20,
            talent_level=self._funzelkram['Fertigkeitswerte'],
            talent_composition=self._funzelkram['Proben'],
            success=gelungen,
            crit=krit,
            quality_level=qualitätsstufen,
            kind_of_test='vollführt',
            modification=modifikator)
        return out

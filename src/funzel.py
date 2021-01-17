# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 17:26:37 2021

@author: reMner
"""

from held import Held


class Funzel(Held):

    def __init__(self, name, funzeligkeit,
                 eigenschaftswerte=[], fertigkeitenwerte=[],
                 funzel_fertigkeiten={}):
        super().__init__(name, eigenschaftswerte, fertigkeitenwerte)

        assert funzeligkeit in ['Priester', 'Pristerin',
                                'Hexer', 'Hexe', 'Zauberer', 'Zauberin'],\
            '{} ist keine unterstützte Rolle.'
        self.rolle = funzeligkeit

        if len(funzel_fertigkeiten.keys()) == 0:
            self._funzelkram = self.__ask_for_funzel_stuff()
        else:
            self._funzelkram = funzel_fertigkeiten

    def __ask_for_funzel_stuff(self, funzel_dict={}):
        clean_read = False
        while not clean_read:
            response = input('Sollen weitere {}'
                             ' aufgenommen werden?\n(j/n) '.format(
                                 self.__funzel_stuff_term(False)))
            if response in ['j', 'n']:
                clean_read = True
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
                funzel_dict[bezeichner] = {'Fertigkeitswert': fertigkeitswert,
                                           'Proben': tuple(eig)}

            # rekursiv nach weitern Zaubern fragen
            return self.__ask_for_funzel_stuff(funzel_dict)
        else:
            return funzel_dict

        def __funzel_stuff_term(self, singular: bool):
            if self.rolle in ['Priesterin', 'Priester']:
                if singular:
                    term = 'Liturgie / Zeremonie'
                else:
                    term = 'Liturgien & Zeremonien'
            elif self.rolle in ['Zauberin', 'Zauberer']:
                if singular:
                    term = 'Zauber / Ritual'
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

        def speichern(self):
            pass

        @classmethod
        def _from_json(cls, name, stats):
            hero = cls(name,
                       list(stats['Eigenschaften'].values()),
                       list(stats['Fertigkeiten'].values()),
                       stats['Funzelfertigkeiten'])
            return hero

        def durchführen(self):
            pass


if __name__ == '__main__':
    jorah = Funzel('Jorah Honorald', 'Priester', [10]*8, [5]*59)

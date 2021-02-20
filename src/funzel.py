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
    """Derived from Held to handle the usage of spell-likes.

    For more details see docs of held.Held

    Basic functionality
    -------------------
    >>> mary = Funzel('Mary Sue', 'Geweihte')
    ==-> Nun Eigenschaften eingeben <-==
        ...
    ==->  Nun Fertigkeiten eingeben  <-==
        ...
    Sollen weitere Liturgien & Zeremonien aufgenommen werden?
    (j/n) j
    Name des/der Liturgie/Zeremonie: Segen
        ...
    >>> print(mary.durchführen('Segen'))
    Mary Sue vollführt Segen (Fertigkeitswert 5).
    Eigenschaften:
        Inuition - Intuition - Klugheit
    Zielwerte:
        [11 11 11]
    Würfelergebnis:
        [2 2 1]
    Ergebnis:	Erfolg mit 2 Qualitätsstufen.

    Parameters
    ----------
    name : str
        Name of the (casting) hero.
    funzeligkeit : str
        Catecory of supernaturlity.
    eigenschaftswerte : list, optional
        List of integer with lenght 8, representing the values for the
        attributes. Are asked in command line dialogue if not specified.
        The default is [].
    fertigkeitenwerte : list, optional
        List of integer with length 59, representing the values for the
        skills/talents. Are asked in command line dialogue if not
        specified.
        The default is [].
    unfähigkeiten : list or set or None, optional
        String representation of incompetent skills/talents.
        The default is None.
    begabungen : list or set or None, optional
        String representation of gifted skills or spell-likes.
        The default is None.
    funzel_fertigkeiten : dict, optional
        Contain information of known spell-likes. Must provide keys 'Proben'
        'Fertigkeistwerte'. See __ask_for_funzel_stuff for more details on
        foramt.
        The default is {}.

        """

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

    @classmethod
    def _from_json(cls, name, stats):
        """Initate a object of Funzel from given `name` and specified `stats`.

        Since incompetences and gifted skills are optional, `stats` is checked
        for those values, if they are not represented in the dict, they point
        to `None`.

        Parameters
        ----------
        name : str
            Used as name for initiated object of type Held.
        stats : dict
            Contain statistics to instantiate hero with all informations.
            Must provide stats:'Eigenschaften' -> a=[int], with len(a)=8
            and stats:'Fertigkeiten' -> b=[int], with len(b)=59
            and stats:'Funzelfertigkeiten' -> dict;
            may contain Values for 'Unfähigkeiten' and 'Begabungen'.

        Returns
        -------
        hero : Funzel
            Initiated hero with spell-like skills.

        """
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
        """Initiate command line dialogue to update gifted and incompetences.

        After confirmation the corresponding sets are updated.
        Call super method and state spell-likes as feasable for the category
        gifted.

        Parameters
        ----------
        weiterhin_zulässig : list, optional
            List of strings representing additional legal skills for gifted
            and incompetences. Enable the permisson of spell-likes for usage
            as gifted skills.
            The default is [].

        Raises
        ------
        ValueError
            Raised when user try to...
                ...set more than 3 gifted skills.
                ...set more than 2 incompetences.
                ...set the same skill as gifted and incompetence.
                ...choose a non legal option (typo, attributes, etc.)

        Returns
        -------
        None.

        """
        super().aktualisiere_besondere_befähigungen(
            weiterhin_zulässig=list(self._funzelkram['Proben'].keys()))

    def durchführen(self, fähigkeit: str, modifikator=0):
        """Perform a test on a certain spell-like w.r.t. skill and attributes.

        Core functionality of this class. Extends the possibilty of helds
        `absolviere` to spell-likes, which folling same principles like
        skill test (roll of 3D20).

        Parameters
        ----------
        fähigkeit : str
            State the spell-like to be tested.
        modifikator : int, optional
            Modification set to the test; negative values for a more difficult,
            positve values for an easier test
            The default is 0.

        Raises
        ------
        KeyError
            Raised when designated spell-like `fähigkeiten` is not found among
            the known ones, i.e. key in `self._funzelkram['Proben']` and
            `self._funzelkram['Fertigkeitswerte']`.

        Returns
        -------
        str
            Formatted result of the skill test.

        """
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

    def speichern(self, dateipfad='C:/Users/49162/Documents/RolePlay/PnP/DSA'):
        """Store character describing dictionaries as json on harddrive.

        File is written as <name>.json, whereby spaces are removed.

        Parameters
        ----------
        dateipfad : str, optional
            Directory to store the char.
            The default is 'C:/Users/49162/Documents/RolePlay/PnP/DSA'.

        Raises
        ------
        OSError
            Raised in cases of problems concerning writing permissions or
            errors in specified path.

        Returns
        -------
        None.

        """
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
        """Show spell-likes, whereby values and compositon are separated.

        Returns
        -------
        str
            Formatted representation.

        """
        title = '{}\'s {}:'.format(self.name, self.__funzel_stuff_term(False))
        return super()._show_pretty_dicts(title, self._funzelkram)

    def __ask_for_funzel_stuff(self,
                               funzel_dict={'Proben': {},
                                            'Fertigkeitswerte': {}}):
        """Initate command line dialogue to recieve spell likes.

        Basic funtionality is described in class docstring.

        Parameters
        ----------
        funzel_dict : dict, optional
            Dictionary to be extend. The default is the expected empty dict
            of a funzels spell-likes.
            The default is {'Proben': {}, 'Fertigkeitswerte': {}}.

        Returns
        -------
        dict
            Updated spell-like dictionary.

        """
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
        """Heleper for handling correct grammar and designation of spell-likes.

        Parameters
        ----------
        singular : bool
            Iff term is expected as sigular; else plural.

        Returns
        -------
        term : str
            Correct designation for spell-likes.

        """
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

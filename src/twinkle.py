# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 17:26:37 2021

@author: Mirko Ulrich
"""

import json
import pathlib

import numpy as np

from hero import Hero


class Twinkle(Hero):
    """Derived from Hero to handle the usage of spell-likes.

    For more details see docs of hero.Hero

    Basic functionality
    -------------------
    >>> mary = Twinkle('Mary Sue', 'Geweihte')
    ==-> Nun Eigenschaften eingeben <-==
        ...
    ==->  Nun Fertigkeiten eingeben  <-==
        ...
    Sollen weitere Liturgien & Zeremonien aufgenommen werden?
    (j/n) j
    Name des/der Liturgie/Zeremonie: Segen
        ...
    >>> print(mary.perform('Segen'))
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
    twinkle_variant : str
        Catecory of supernaturality.
    attribute_values : list, optional
        List of integer with lenght 8, representing the values for the
        attributes. Are asked in command line dialogue if not specified.
        The default is [].
    skill_values : list, optional
        List of integer with length 59, representing the values for the
        skills/talents. Are asked in command line dialogue if not
        specified.
        The default is [].
    incompetences : list or set or None, optional
        String representation of incompetent skills/talents.
        The default is None.
    gifted : list or set or None, optional
        String representation of gifted skills or spell-likes.
        The default is None.
    twinkle_abilities : dict, optional
        Contain information of known spell-likes. Must provide keys 'Proben'
         and 'Fertigkeistwerte'. See __ask_for_twinkle_stuff for more details
         on format.
        The default is {}.

        """

    def __init__(self, name, twinkle_variant,
                 attribute_values=[], skill_values=[],
                 incompetences=None, gifted=None,
                 twinkle_abilities={}):
        assert twinkle_variant in ['Geweihter', 'Geweihte',
                                'Hexer', 'Hexe', 'Zauberer', 'Zauberin'],\
            '{} ist keine unterstützte Rolle.'.format(twinkle_variant)
        super().__init__(name, attribute_values, skill_values,
                         incompetences, gifted)
        self.profession = twinkle_variant

        if len(twinkle_abilities.keys()) == 0:
            self._twinkle_stuff = self.__ask_for_twinkle_stuff()
        else:
            self._twinkle_stuff = twinkle_abilities

    @classmethod
    def _from_json(cls, name, stats):
        """Initate a object of Twinkle from given `name` and specified `stats`.

        Since incompetences and gifted skills are optional, `stats` is checked
        for those values, if they are not represented in the dict, they point
        to `None`.

        Parameters
        ----------
        name : str
            Used as name for initiated object of type Twinkle.
        stats : dict
            Contain statistics to instantiate hero with all informations.
            Must provide stats:'Eigenschaften' -> a=[int], with len(a)=8
            and stats:'Fertigkeiten' -> b=[int], with len(b)=59
            and stats:'Funzelfertigkeiten' -> dict;
            may contain Values for 'Unfähigkeiten' and 'Begabungen'.

        Returns
        -------
        hero : TWinkle
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

    def analyze_spelllike(self, spell, modifier=0):
        """Visualize the probability of spell-like with plot and string.

        Wrapper for `Hero._analyze_success`, specifies the source for the
        combination of attributes.

        Parameters
        ----------
        spell : str
            State the spell-like to be analyzed.
        modifier : int, optional
            Modification set to the test; negative values for a more difficult,
            positve values for an easier test
            The default is 0.

        Returns
        -------
        str
            Formatted describtion of quality level distribution for specified
            spell-like.

        """
        return self._analyze_success(
            spell,
            attribute_source=self._twinkle_stuff['Proben'],
            skill_value_source=self._twinkle_stuff['Fertigkeitswerte'],
            modifier=modifier)

    def update_special_abilities(self, also_permitted=[]):
        """Initiate command line dialogue to update gifted and incompetences.

        After confirmation the corresponding sets are updated.
        Call super method and state spell-likes as feasable for the category
        gifted.

        Parameters
        ----------
        also_permitted : list, optional
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
        super().update_special_abilities(
            also_permitted=list(self._twinkle_stuff['Proben'].keys()))

    def delete_spelllike(self, spell):
        """Remove given spell-like from twinkles list of abilities.

        Parameters
        ----------
        spell : str
            Spell-like to remove. Must be key in `self._twinkle_stuff[..]`.

        Raises
        ------
        KeyError
            Iff argument `spell` is not a known spell-like.

        Returns
        -------
        None.

        """
        try:
            check = self._twinkle_stuff['Proben'][spell]
            value = self._twinkle_stuff['Fertigkeitswerte'][spell]
        except KeyError:
            raise KeyError('{} ist kein/e bekannte/r/s {}.'.format(
                spell, self.__twinkle_stuff_term(singular=True)))

        msg = ('Löschen von {} mit Proben auf {} und'
               ' Fertigkeitswert {}?\n(j/n) ')
        response = self._clean_read(
                text=msg.format(spell,check,value),     
                legal_response=['j', 'n'])
        if response == 'j':
            self._twinkle_stuff['Proben'].pop(spell)
            self._twinkle_stuff['Fertigkeitswerte'].pop(spell)
            print('{} wurde gelöscht.'.format(spell))
        else:
            print('Keine Werte gelöscht.')

    def add_spelllike(self):
        """Initiate command line dialog to add new spell-like; may see init."""
        self._twinkle_stuff = self.__ask_for_twinkle_stuff(
            twinkle_dict=self._twinkle_stuff)

    def update_spelllike(self, spell: str, by=1):
        """Update value for specified spell-like by given integer.

        Parameters
        ----------
        spell : str
            Talent/skill to update. Must be among the keys of
            `self._twinkle_stuff['Fertigkeitswerte']`.
        by : int, optional
            Value for additive manipulation.
            The default is 1.

        Raises
        ------
        ValueError
            Iff updated skill value would violent legal limits.
        KeyError
            Iff argument `spell` is not among the spell-likes.

        Returns
        -------
        None.

        """
        assert isinstance(by, int),\
            'Entwicklungsdiffernez muss als ganze Zahl gegeben sein.'

        try:
            old_val = self._twinkle_stuff['Fertigkeitswerte'][spell]
            new_val = old_val + by
            if 0 <= new_val <= 25:
                msg = 'Fertigkeitswert von {} von {} auf {} setzen?\n(j/n) '
                res = self._clean_read(msg.format(spell, old_val, new_val),
                                       legal_response=['j', 'n'])
                if res == 'j':
                    self._twinkle_stuff['Fertigkeitswerte'][spell] = new_val
                    print('Wert angepasst.')
                else:
                    print('Keine Änderungen vorgenommen.')
            else:
                raise ValueError('Entwickelter Wert muss im '
                                 'Bereich 0 bis 25 liegen.')
        except KeyError:
            raise KeyError('{} ist kein/e gültige/r/s {}.'.format(
                spell, self.__twinkle_stuff_term(singular=True)))

    def perform(self, spell_like: str, modifier=0):
        """Perform a test on a certain spell-like w.r.t. skill and attributes.

        Core functionality of this class. Extends the possibilty of helds
        `absolviere` to spell-likes, which folling same principles like
        skill test (roll of 3D20).

        Parameters
        ----------
        spell_like : str
            State the spell-like to be tested.
        modifikator : int, optional
            Modification set to the test; negative values for a more difficult,
            positve values for an easier test
            The default is 0.

        Returns
        -------
        str
            Formatted result of the skill test.

        """
        # estimate objectives for rolling
        objective, impossible = self._estimae_objective(
            talent=spell_like, modifier=modifier,
            attribute_source=self._twinkle_stuff['Proben'])
    
        if impossible:
            msg = ('Die Erschwernis von {} '
                   'macht diese Probe unmöglich.'.format(abs(modifier)))
            return msg

        _3w20 = np.random.randint(1, 21, 3)

        # Zufallsereignis auswerten
        succ, crit, quality_level, _ = self._perform_test(
            aim=objective, random_event=_3w20,
            skill_level=self._twinkle_stuff['Fertigkeitswerte'][spell_like],
            gifted=(spell_like in self._gifted))

        # Ausgabe bestimmen
        out = self._format_outcome(
            skill=spell_like,
            goals=objective,
            random_event=_3w20,
            talent_level=self._twinkle_stuff['Fertigkeitswerte'],
            talent_composition=self._twinkle_stuff['Proben'],
            success=succ,
            crit=crit,
            quality_level=(quality_level, quality_level),
            kind_of_test='vollführt',
            modification=modifier)
        return out

    def save(self, directory='C:/Users/49162/Documents/RolePlay/PnP/DSA'):
        """Store character describing dictionaries as json on harddrive.

        File is written as <name>.json, whereby spaces are removed.

        Parameters
        ----------
        directory : str, optional
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
        directory = pathlib.Path(directory)
        if directory.exists() and directory.is_dir():
            file = '{}.json'.format(self.name.replace(' ', '_'))
            data_to_dump = {'Profession': self.profession,
                            'Eigenschaften': self._attributes,
                            'Fertigkeiten': self._skills,
                            'Funzelfertigkeiten': self._twinkle_stuff,
                            'Begabungen': list(self._gifted),
                            'Unfähigkeiten': list(self._incompetences)}
            with open(pathlib.Path(directory, file),
                      'w') as file:
                json.dump(data_to_dump, file)
        else:
            raise OSError('Mit gültigem Pfad erneut versuchen.'
                          ' Eventuell Schreibrechte überprüfen.')

    def show_supernatural_abilities(self):
        """Show spell-likes, whereby values and compositon are separated.

        Returns
        -------
        str
            Formatted representation.

        """
        title = '{}\'s {}:'.format(self.name, self.__twinkle_stuff_term(False))
        return super()._show_pretty_dicts(title, self._twinkle_stuff)

    def __ask_for_twinkle_stuff(self,
                               twinkle_dict={'Proben': {},
                                            'Fertigkeitswerte': {}}):
        """Initate command line dialogue to recieve spell likes.

        Basic funtionality is described in class docstring.

        Parameters
        ----------
        twinkle_dict : dict, optional
            Dictionary to be extend. The default is the expected empty dict
            of a twinkle spell-likes.
            The default is {'Proben': {}, 'Fertigkeitswerte': {}}.

        Returns
        -------
        dict
            Updated spell-like dictionary.

        """
        response = super()._clean_read(
            text='Sollen weitere {} aufgenommen werden?\n(j/n) '.format(
                self.__twinkle_stuff_term(False)),
            legal_response=['j', 'n'])

        if response == 'j':                         # record more twinkle stuff
            # Name des Zaubers oder Wirkung
            designation = input('Name des/der {}: '.format(
                self.__twinkle_stuff_term(True)))
            # die drei Eigenschaften für die Probe
            att = []
            while len(att) < 3:
                val = input('{}. Eigenschaft für {}: '.format(len(att)+1,
                                                              designation))
                if val in self._attributes.keys():
                    att.append(val)
                else:
                    print('{} ist keine gültige Eigenschaft.'.format(val))
            # Fertigkeitswert des Zaubers / der Wirkung
            clean_read = False
            while not clean_read:
                try:
                    fertigkeitswert = int(
                        input('Fertigkeitswert für {}: '.format(designation))
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
                                     designation, fertigkeitswert, *att))
                if response in ['j', 'n']:
                    clean_read = True
            if response == 'j':
                twinkle_dict['Proben'][designation] = tuple(att)
                twinkle_dict['Fertigkeitswerte'][designation] = fertigkeitswert

            # rekursiv nach weitern Zaubern fragen
            return self.__ask_for_twinkle_stuff(twinkle_dict)
        else:
            return twinkle_dict

    def __twinkle_stuff_term(self, singular: bool):
        """Helper for handling correct grammar and designation of spell-likes.

        Parameters
        ----------
        singular : bool
            Iff term is expected as singular; else plural.

        Returns
        -------
        term : str
            Correct designation for spell-likes.

        """
        if self.profession in ['Geweihte', 'Geweihter']:
            if singular:
                term = 'Liturgie/Zeremonie'
            else:
                term = 'Liturgien & Zeremonien'
        elif self.profession in ['Zauberin', 'Zauberer']:
            if singular:
                term = 'Zauber/Ritual'
            else:
                term = 'Zauber & Rituale'
        elif self.profession in ['Hexe', 'Hexer']:
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

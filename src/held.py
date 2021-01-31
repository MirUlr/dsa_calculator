# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 09:27:20 2021

@author: Mirko Ulrich
"""

import json
import pathlib

import numpy as np


class Held():
    """Baseclass for characters from the rpg `Das Shwarze Auge` (DSA).

    This class is motivated by the need for automatic evaluation of test,
    which is executed via the roll of three dices with twenty faces. This
    independent random vector of three components must be lower than the
    heros values in the corresponding attributes. See official rules at
    https://ulisses-regelwiki.de/index.php/GR_Proben.html

    Basic funtionality
    ------------------
    >>> from held import Held
    >>> mary = Held('Mary Sue')
    ==-> Nun Eigenschaften eingeben <-==
        ...
    ==->  Nun Fertigkeiten eingeben  <-==
        ...
    >>> print(mary.absoviere('Zechen', modifikator=-1))
    Mary Sue absolviert eine Probe auf Zechen (Fertigkeistwert 5), um 1
    erschwert.
    Eigenschaften:
        Klugheit - Konstitution - Körperkraft
    Zielwerte:
        [12 11 12]
    Würfelergebnis:
        [3 2 9]
    Ergebnis:   Erfolg mit 2 Qualitätsstufen

    Parameters
    ----------
    name : str
        Name of the hero.
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

    Raises
    ------
    TypeError
        Raised when `unfähigkeiten` or `begabungen` are not given as set, list
        or None.

    """
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
        'Fischen & Angeln': ('Fingerfertigkeit', 'Gewandtheit',
                             'Konstitution'),
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
        'Lederbearbeitung': ('Fingerfertigkeit', 'Gewandtheit',
                             'Konstitution'),
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

    def __init__(self, name, eigenschaftswerte=[], fertigkeitenwerte=[],
                 unfähigkeiten=None, begabungen=None):
        self.name = name
        self._eigenschaften = dict.fromkeys(
            ['Mut', 'Klugheit', 'Intuition', 'Charisma', 'Fingerfertigkeit',
             'Gewandtheit', 'Konstitution', 'Körperkraft'])
        self._fertigkeiten = dict.fromkeys(
            list(self.FERTIGKEITSPROBEN.keys()))

        if len(eigenschaftswerte) != len(self._eigenschaften):
            print('==->  Nun Eigenschaften eingeben  <-==')
            eigenschaftswerte = self.__ask_for_values(self._eigenschaften,
                                                      (1, 19))
        self._eigenschaften = {
            list(self._eigenschaften.keys())[i]: eigenschaftswerte[i]
            for i in range(len(eigenschaftswerte))}

        if len(fertigkeitenwerte) != len(self._fertigkeiten):
            print('==->  Nun Fertigkeiten eingeben  <-==')
            fertigkeitenwerte = self.__ask_for_values(self._fertigkeiten,
                                                      (0, 25))
        self._fertigkeiten = {
            list(self._fertigkeiten.keys())[i]: fertigkeitenwerte[i]
            for i in range(len(fertigkeitenwerte))}

        if unfähigkeiten is None:
            self._unfähigkeiten = set()
        else:
            if isinstance(unfähigkeiten, set):
                self._unfähigkeiten = unfähigkeiten
            elif isinstance(unfähigkeiten, list):
                self._unfähigkeiten = set(unfähigkeiten)
            else:
                raise TypeError('`unfähigkeiten` wird als '
                                'set oder list erwartet')

        if begabungen is None:
            self._begabungen = set()
        else:
            if isinstance(begabungen, set):
                self._begabungen = begabungen
            elif isinstance(begabungen, list):
                self._begabungen = set(begabungen)
            else:
                raise TypeError('`begabungen` wird als set oder list erwartet')

    @classmethod
    def laden(cls, charakter,
              verzeichnis='C:/Users/reMner/Desktop/PnP/DSA'):
        """Load character from harddrive and returns corresponding Held object.

        Parameters
        ----------
        charakter : str
            Name of the character to be loaded. Althogh underscore style is
            used in file naming, the intended name may be used.
        verzeichnis : str, optional
            Specifies directory to load <name>.json from.
            The default is 'C:/Users/reMner/Desktop/PnP/DSA'.

        Raises
        ------
        ValueError
            Raised when specified hero is not found in given directory.

        Returns
        -------
        Held
            Initiated hero.

        """
        final_file = pathlib.Path(verzeichnis,
                                  (charakter + '.json').replace(' ', '_'))
        if final_file.exists() and final_file.is_file():
            with open(final_file, 'r') as source:
                data = json.load(source)
            return cls._from_json(name=charakter.replace('_', ' '),
                                  stats=data)
        else:
            raise ValueError('Keine gültigen Daten gefunden.')

    @classmethod
    def _from_json(cls, name, stats):
        """Initate an instance of Held from given `name` and specified `stats`.

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
            and stats:'Fertigkeiten' -> b=[int], with len(b)=59;
            may contain Values for 'Unfähigkeiten' and 'Begabungen'.

        Returns
        -------
        hero : Held
            Initiated hero.

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
                   list(stats['Eigenschaften'].values()),
                   list(stats['Fertigkeiten'].values()),
                   incompetences,
                   gifted_talents)
        return hero

    def absolviere(self, talent, modifikator=-0):
        """Perform a test on a certin talent, w.r.t. skikll value and modifier.

        Core functionality.
        This method allow the execution of the dsa signature content: the
        3D20 test. For more details see Held._perform_test or the official
        rules at https://ulisses-regelwiki.de/index.php/GR_Proben.html

        Parameters
        ----------
        talent : str
            State the talent/skill to be tested.
        modifikator : int, optional
            Modification set to the test; negative values for a more difficult,
            positve values for an easier test
            The default is 0.


        Raises
        ------
        ValueError
            Raised when specified talent is not legal, i.e. is not a key in
            FERTIGKEITSPROBEN.

        Returns
        -------
        str
            Formatted result of the skill test.

        """
        try:
            zielwerte = np.array(
                [self._eigenschaften[eig]
                 for eig in self.FERTIGKEITSPROBEN[talent]])
            add_cap_19 = np.vectorize(
                lambda x: min(19, x + modifikator)
                )
            zielwerte = add_cap_19(zielwerte)
        except KeyError:
            raise ValueError('{} ist keine'
                             ' gültige Fertigkeit.'.format(talent))

        if any(zielwerte < 1):                  # unmögliche Proben detektieren
            msg = ('Die Erschwernis von {} '
                   'macht diese Probe unmöglich.'.format(abs(modifikator)))
            return msg

        _3w20 = np.random.randint(1, 21, 3)

        # Zufallsereignis auswerten
        gelungen, krit, qualitätsstufen = self._perform_test(
            aim=zielwerte, random_event=_3w20,
            skill_level=self._fertigkeiten[talent],
            gifted=(talent in self._begabungen),
            incompetent=(talent in self._unfähigkeiten))

        # Ausgabe bestimmen
        out = self._format_outcome(
            skill=talent,
            goals=zielwerte,
            random_event=_3w20,
            talent_level=self._fertigkeiten,
            talent_composition=self.FERTIGKEITSPROBEN,
            success=gelungen,
            crit=krit,
            quality_level=qualitätsstufen,
            modification=modifikator)
        return out

    def aktualisiere_besondere_befähigungen(self,
                                            weiterhin_zulässig=[]):
        """Initiate command line dialogue to update gifted and incompetences.

        After confirmation the corresponding sets are updated.

        Parameters
        ----------
        weiterhin_zulässig : list, optional
            List of strings representing additional legal skills for gifted
            and incompetences. Enable derived classes to allow spell-likes as
            gifted skills.
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
        # Whether gifts shall be updated
        val = self._clean_read(text='Begabungen aktualisieren?\n(j/n) ',
                               legal_response=['j', 'n'])
        if val == 'j':
            temp = self._show_and_update_set(
                '{}\'s Begabungen:'.format(self.name),
                self._begabungen)
            if len(temp) > 3:
                raise ValueError('Nicht mehr als 3 Begabungen erlaubt.')
            for t in temp:
                in_skills = t in self.FERTIGKEITSPROBEN.keys()
                in_further_skills = t in weiterhin_zulässig
                if not in_skills and not in_further_skills:
                    raise ValueError('{} ist keine zulässige'
                                     ' Fertigkeit.'.format(t))
            if temp.isdisjoint(self._unfähigkeiten):
                self._begabungen = temp
            else:
                raise ValueError('Begabungen und Unfähigkeiten'
                                 ' dürfen sich nicht überlappen.')

        # whether inability shall be updated
        val = self._clean_read(text='Unfähigkeiten aktualisieren?\n(j/n) ',
                               legal_response=['j', 'n'])
        if val == 'j':
            temp = self._show_and_update_set(
                '{}\'s Unfähigkeiten:'.format(self.name),
                self._unfähigkeiten)
            if len(temp) > 2:
                raise ValueError('Nicht mehr als 2 Unfähigkeiten erlaubt.')
            for t in temp:
                if t not in self.FERTIGKEITSPROBEN.keys():
                    raise ValueError('{} ist keine'
                                     ' zulässige Fertigkeit.'.format(t))
            if temp.isdisjoint(self._begabungen):
                self._unfähigkeiten = temp
            else:
                raise ValueError('Begabungen und Unfähigkeiten'
                                 ' dürfen sich nicht überlappen.')

        val = self._clean_read(
            text='Weitere Aktualisierungen vornehmen?\n(j/n) ',
            legal_response=['j', 'n'])

        # whether more updates shall be happen
        if val == 'j':
            self.aktualisiere_besondere_befähigungen(
                weiterhin_zulässig=weiterhin_zulässig)

    def speichern(self, dateipfad='C:/Users/reMner/Desktop/PnP/DSA'):
        """Store character describing dictionaries as json on harddrive.

        File is written as <name>.json, whereby spaces are removed.

        Parameters
        ----------
        dateipfad : str, optional
            Directory to store the char.
            The default is 'C:/Users/reMner/Desktop/PnP/DSA'.

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
            data_to_dump = {'Eigenschaften': self._eigenschaften,
                            'Fertigkeiten': self._fertigkeiten,
                            'Begabungen': list(self._begabungen),
                            'Unfähigkeiten': list(self._unfähigkeiten)}
            with open(pathlib.Path(dateipfad, file),
                      'w') as file:
                json.dump(data_to_dump, file)
        else:
            raise OSError('Mit gültigem Pfad erneut versuchen.'
                          ' Eventuell Schreibrechte überprüfen.')

    def teste(self, eigenschaft, modifikator=0):
        """Perform an attribute check, meaning a 1D20 roll.

        Parameters
        ----------
        eigenschaft : str
            Attribute to be checked.
        modifikator : int, optional
            Modification set to the test; negative values for a more difficult,
            positve values for an easier test
            The default is 0.

        Returns
        -------
        msg : str
            Formatted result of the attribute check.

        """
        assert eigenschaft in self._eigenschaften.keys(),\
            '{} ist keine gültige Eigenschaft.'.format(eigenschaft)
        eigenschaftswert_mod = min(
            self._eigenschaften[eigenschaft] + modifikator, 19)
        _1w20 = np.random.randint(1, 21, 1)

        erfolg, kritisch, _ = self._perform_test(
            aim=np.array(eigenschaftswert_mod),
            random_event=_1w20)

        msg = '{} testet {} ({})'.format(
                self.name, eigenschaft, self._eigenschaften[eigenschaft])
        if modifikator == 0:
            msg += ':\n'
        elif modifikator > 0:
            msg += ', erleichtert um {}:\n'.format(str(abs(modifikator)))
        elif modifikator < 0:
            msg += ', erschwert um {}:\n'.format(str(abs(modifikator)))

        if erfolg:
            msg += '\nGeschafft mit einem Wurf von {}.'.format(*_1w20)
        else:
            msg += '\nNicht geschafft mit einem Wurf von {}.'.format(*_1w20)

        return msg

    def zeige_besondere_befähigungen(self):
        """Show talents which are marked as gifted or incompetent.

        Returns
        -------
        out : str
            Formatted representation.

        """
        msg_1 = '{}\'s Begabungen:'.format(self.name)
        line = '='*len(msg_1)
        msg_1 += '\n{}\n\t'.format(line)
        for t in self._begabungen:
            msg_1 += '{} '.format(t)

        msg_2 = '{}\'s Unfähigkeiten:'.format(self.name)
        line = '='*len(msg_2)
        msg_2 += '\n{}\n\t'.format(line)
        for u in self._unfähigkeiten:
            msg_2 += '{} '.format(u)

        out = msg_1 + '\n' + msg_2
        return out

    def zeige_eigenschaften(self):
        """Show attributes and values.

        Returns
        -------
        str
            Formatted representation.

        """
        return self._show_pretty_dicts(
            '{}\'s Eigenschaften:'.format(self.name), self._eigenschaften)

    def zeige_fertigkeiten(self):
        """Show skills and values.

        Returns
        -------
        str
            Formatted representation.

        """
        return self._show_pretty_dicts(
            '{}\'s Fertigkeiten:'.format(self.name), self._fertigkeiten)

    def get_gifted_skills_gui(self):
        """Getter for gifted skills(`Begabungen`); concerning GUI.

        Returns
        -------
        gifted_skills : list
            List of strings representing the heros' gifted skills.

        """
        gifted_skills = []
        for begabung in self._begabungen:
            gifted_skills.append(self._tamper_designation(begabung))
        return gifted_skills

    def get_incompetent_skills_gui(self):
        """Getter for incompetences(`Unfähigkeiten`); concerning GUI.

        Returns
        -------
        incompetent_skills : list
            List of strings representing the heros' incompetences.

        """
        incompetent_skills = []
        for unfähigkeit in self._unfähigkeiten:
            incompetent_skills.append(self._tamper_designation(unfähigkeit))
        return incompetent_skills

    def _format_outcome(self, skill: str, goals, random_event,
                        talent_level: dict,
                        talent_composition: dict,
                        success: bool, crit: bool, quality_level: int,
                        kind_of_test='absolviert eine Probe auf',
                        modification=0):
        """Summarize the results of a (3D20) roll with all necessary values.

        Parameters
        ----------
        skill : str
            Talent which was tested.
        goals : numpy.ndarry
            Values to achieve lower rolls.
        random_event : numpy.ndarray
            Representing the roll.
        talent_level : dict
            Must contain `skill` as key.
        talent_composition : dict
            Must contain `skill` as key.
        success : bool
            Iff test was passed.
        crit : bool
            Iff test was passed outstanding (success or fail).
        quality_level : int
            Measurement of success (if accomplished).
        kind_of_test : str, optional
            Allows to formate also spell-likes from derived classes.
            The default is 'absolviert eine Probe auf'.
        modification : int, optional
            Modification set to the test; negative values for a more difficult,
            positve values for an easier test
            The default is 0.

        Returns
        -------
        out : str
            Summarized information.

        """
        out = ''
        if modification == 0:
            test = '{} {} {} (Fertigkeitswert {}).'
        else:
            if modification < 0:
                test = '{} {} {} (Fertigkeitswert {}), um ' +\
                    str(abs(modification)) + ' erschwert.'
            else:
                test = '{} {} {} (Fertigkeitswert {}), um ' +\
                    str(abs(modification)) + ' erleichtert.'
        out += test.format(self.name, kind_of_test, skill,
                           talent_level[skill])

        goal_to_aim = ('\nEigenschaften:\n\t{} - {} -'
                       ' {}\nZielwerte:\n\t{}').format(
            *talent_composition[skill], goals)
        out += '\n' + goal_to_aim

        outcome_rng = 'Würfelergebnis:\n\t{}\n'.format(random_event)
        out += '\n' + outcome_rng

        if skill in self._begabungen:
            kind_of_result = 'Ergebnis der Begabung'
        elif skill in self._unfähigkeiten:
            kind_of_result = 'Ergebnis der Unfähigkeit'
        else:
            kind_of_result = 'Ergebnis'

        if success:
            if crit:
                final_result = ('{}:\tKritischer Erfolg mit {} '
                                'Qualitätsstufen.\t:-D'.format(
                                    kind_of_result,
                                    quality_level))
            else:
                final_result = ('{}:\tErfolg mit '
                                '{} Qualitätsstufen.'.format(
                                    kind_of_result,
                                    quality_level))
        else:
            if crit:
                final_result = '{}:\tPatzer\t>:-|'.format(kind_of_result)
            else:
                final_result = '{}:\tFehlschlag'.format(kind_of_result)
        out += '\n' + final_result

        return out

    def _perform_test(self, aim, random_event, skill_level=0,
                      gifted=False, incompetent=False):
        """Evalutae the performance of random event and measure the success.

        Core functionality of this class, evaluate the signature content from
        DA: the 3D20 test. All rolls that surpass the corresponding value in
        `aim` must be compensted with `skill_level`. If this is possible, the
        test is consierd as success.
        See https://ulisses-regelwiki.de/index.php/GR_Proben.html for more
        information.
        Special cases: If `random_event` contain more than one ones or
        twenties, the test is accomplished with a critical result and the test
        is passed (ones) or failed (twenty) independet from the spare points
        from `skill_level`.
        May also be used for nDm-test against a target value `aim`, as long as
        `skill_level` equals zero.

        Parameters
        ----------
        aim : numpy.ndarray
            Target values (integer) to fall below. Must match the length of
            `random_event`.
        random_event : numpy.ndarray
            Roll to be evaluated if (and how good) accomplished. Must match the
            length of `aim`.
        skill_level : int, optional
            Number of points to compensate high rolls.
            The default is 0.
        gifted : bool, optional
            Random event is preprocessed: The highest roll will be rerolled and
            the better (lower) event will be taken for further process.
            See https://ulisses-regelwiki.de/index.php/V_Begabung.html
            The default is False.
        incompetent : bool, optional
            Random event is preprocessed: The lowest (best) roll will be
            rerolled and then taken for further process. Therefore
            `random_event` actual may be improved.
            See http://ulisses-gamereference.com/index.php/N_Unf%C3%A4hig.html
            The default is False.

        Raises
        ------
        ValueError
            Raised if `random_event` shall be preprocessed in both ways.

        Returns
        -------
        success : bool
            True iff test was accomplished.
        critical : bool
            True iff result is outstanding (either success or failure).
        quality_level : int
            Measurement of success.

        """
        if gifted and incompetent:
            raise ValueError('A test can not be taken on a talent, which'
                             ' is considered gifted an incompetent at the'
                             ' same time.')

        if incompetent:           # estimate and execute reroll of imcompetence
            idx = np.argmin(random_event)
            random_event[idx] = np.random.randint(1, 21)

        compensation = random_event - aim
        compensation[compensation < 0] = 0

        if gifted:                          # estimate reroll for gifted skills
            idx = np.argmax(compensation)
            reroll = np.random.randint(1, 21)
            better_roll = min(random_event[idx], reroll)
            random_event[idx] = better_roll
            # recursive call with updated rand toggled gifted flag
            return self._perform_test(aim=aim, random_event=random_event,
                                      skill_level=skill_level,
                                      gifted=False)

        spare = skill_level - sum(compensation)

        fail_copy = random_event.copy()
        fail_copy[fail_copy != 20] = 0
        crit_fail = sum(fail_copy) > 20

        win_copy = random_event.copy()
        win_copy[win_copy != 1] = 0
        crit_win = sum(win_copy) > 1

        success = ((spare >= 0) or crit_win) and not crit_fail

        critical = crit_win or crit_fail

        if crit_win:
            spare = max(spare, 0)
            quality_level = self.__determine_quality_level(spare)
            quality_level *= 2
        else:
            quality_level = self.__determine_quality_level(spare)

        return success, critical, quality_level

    def _show_and_update_set(self, title, group):
        """Initate command line dialogue (german) to update given set.

        User get `group` displayed and asked for an element to update. If the
        given input is already in `group`, it will be removed from that set,
        else the given input is added to the set. In both cases a confirmation
        is asked for.

        Parameters
        ----------
        title : str
            Is displayed to user before `group` is shown.
        group : set
            Set to be updated.

        Returns
        -------
        group : set
            Updated copy of `group`.

        """
        group = group.copy()
        print('{}\n{}'.format(title, '='*len(title)))
        print(group)
        val = input('Aktualisiere um Element: ')
        if val in group:
            confirm = self._clean_read('{} entfernen?\n(j/n) '.format(val),
                                       ['j', 'n'])
            if confirm == 'j':
                group.discard(val)
        else:
            confirm = self._clean_read('{} hinzufügen?\n(j/n) '.format(val),
                                       ['j', 'n'])
            if confirm == 'j':
                group.add(val)
        return group

    def _show_pretty_dicts(self, title, dictionary, alphabetical_order=True,
                           depth=1):
        """Formate dictionary to pleasant readable string.

        Parameters
        ----------
        title : str
            Prefix and first line of formulated string.
        dictionary : dict
            Dictionary to display.
        alphabetical_order : bool, optional
            True <=> key-value-pairs are shown in the keys alphabetical order.
            The default is True.
        depth : int, optional
            Used for nested dictionaries. Regulate underlines and indentation.
            The default is 1.

        Returns
        -------
        msg : str
            Pretty print version of dictionary.

        """
        gifted = ' (+)'
        incomp = ' (-)'
        msg = ''
        list_of_keys = list(dictionary.keys())
        if alphabetical_order:
            list_of_keys.sort()
        if depth == 1:
            underline = '\n' + '=' * len(title)
        elif depth == 2:
            underline = '\n' + '-' * len(title)
        else:
            underline = ''
        msg += ('\n' + title + underline)
        for key in list_of_keys:
            if isinstance(dictionary[key], dict):
                value = str(self._show_pretty_dicts(
                    title=key,
                    dictionary=dictionary[key],
                    depth=depth+1))
                msg += ('\t'*depth + value)
            else:
                value = str(dictionary[key])
                if key in self._unfähigkeiten:
                    msg += ('\n' + key + incomp + ':\n' + '\t'*depth + value)
                elif key in self._begabungen:
                    msg += ('\n' + key + gifted + ':\n' + '\t'*depth + value)
                else:
                    msg += ('\n' + key + ':\n' + '\t'*depth + value)
        return msg

    @staticmethod
    def _clean_read(text, legal_response):
        """Helperfunction for command line interaction.

        Parameters
        ----------
        text : str
            Message to display user in console.
        legal_response : list
            List of legal responses. Input is rejected iff it does not occure
            in this list.

        Returns
        -------
        val : str
            Legal user response on displayed message.

        """
        clean_read = False
        while not clean_read:
            val = input(text)
            if val in legal_response:
                clean_read = True
        return val

    @staticmethod
    def _tamper_designation(skill):
        """Transform a given string for GUI concerns.

        In general the given string is changed to lower cases and umlauts are
        replaced. If the given `skill` corresponds to one of the formulated
        special cases, then the spechial transformation is applied.

        Parameters
        ----------
        skill : str
            String to transform, expected to be a skill (`Fertikeit`) or
            identifier of a spell-like (from derived Funzel).

        Returns
        -------
        out : str
            Transformed string.

        """
        special_cases = {'Bekehren & Überzeugen': 'bekehren',
                         'Fischen & Angeln': 'angeln',
                         'Brett- & Glücksspiel': 'brettspiel',
                         'Götter & Kulte': 'kulte',
                         'Sagen & Legenden': 'sagen',
                         'Boote & Schiffe': 'boote',
                         'Heilkunde Gift': 'heilenGift',
                         'Heilkunde Krankheiten': 'heilenKrankhei',
                         'Heilkunde Seele': 'heilenSeele',
                         'Heilkunde Wunden': 'heilenWunden',
                         'Malen & Zeichen': 'malen'}
        if skill in special_cases.keys():
            out = special_cases[skill]
        else:
            umlaute = {'ä': 'ae', 'ö': 'oe', 'ü': 'ue'}
            out = skill.lower()

            for u in umlaute:
                out = out.replace(u, umlaute[u])

        return out

    @staticmethod
    def __ask_for_values(dictionary, limits=(-float('inf'), float('inf'))):
        """Initaialize command line dialogue to determine dict's values.

        Parameters
        ----------
        dictionary : dict
            Dictionary which values shall be determined by user.
        limits : 2-tuple, optional
            Set upper and lower limit for recieved values. Values which violent
            these limits are rejected and the user is informed about the limits
            and asked again for that value.
            The default is (-float('inf'), float('inf')).

        Returns
        -------
        values : list
            List of integer values, corresponding to the order of the keys.

        """
        values = []
        for key in dictionary.keys():
            clean_read = False
            while not clean_read:
                try:
                    val = int(input('Wert für {} eingeben:\t'.format(key)))
                    if val < limits[0] or limits[1] < val:
                        print(
                            'Achtung:\tWert muss sich in Bereich '
                            'von {} bis {} bewegen'.format(*limits))
                    else:
                        clean_read = True
                except ValueError:
                    print('Achtung:\tWert muss als Integer lesbar sein.')
            values.append(val)
        return values

    @staticmethod
    def __determine_quality_level(spare_points):
        """Discretize the success from spare points to quality level.

        In DSA the success of a test is measured in terms of spare points,
        whereby the inital points represent the skill value. For comparrability
        and further evaluation these points are discretize into quality level.
        See https://ulisses-regelwiki.de/index.php/GR_Proben.html for more
        informations.

        Parameters
        ----------
        spare_points : int
          Amount of skill points, which were not used for comensation.

        Returns
        -------
        quality_level : int
            Measurement of success. -1 <=> input messed up.

        """
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

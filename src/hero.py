# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 09:27:20 2021

@author: Mirko Ulrich
"""

import json
import multiprocessing
import pathlib

import numpy as np
import pandas as pd

import plottery

class Hero():
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

    Raises
    ------
    TypeError
        Raised when `incompetences` or `gifted` are not given as set, list
        or None.

    """
    SKILL_CHECKS = {
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

    def __init__(self, name, attribute_values=[], skill_values=[],
                 incompetences=None, gifted=None):
        self.name = name
        self._attributes = dict.fromkeys(
            ['Mut', 'Klugheit', 'Intuition', 'Charisma', 'Fingerfertigkeit',
             'Gewandtheit', 'Konstitution', 'Körperkraft'])
        self._skills = dict.fromkeys(
            list(self.SKILL_CHECKS.keys()))

        if len(attribute_values) != len(self._attributes):
            print('==->  Nun Eigenschaften eingeben  <-==')
            attribute_values = self.__ask_for_values(self._attributes,
                                                      (1, 19))
        self._attributes = {
            list(self._attributes.keys())[i]: attribute_values[i]
            for i in range(len(attribute_values))}

        if len(skill_values) != len(self._skills):
            print('==->  Nun Fertigkeiten eingeben  <-==')
            skill_values = self.__ask_for_values(self._skills,
                                                      (0, 25))
        self._skills = {
            list(self._skills.keys())[i]: skill_values[i]
            for i in range(len(skill_values))}

        if incompetences is None:
            self._incompetences = set()
        else:
            if isinstance(incompetences, set):
                self._incompetences = incompetences
            elif isinstance(incompetences, list):
                self._incompetences = set(incompetences)
            else:
                raise TypeError('`incompetences` wird als '
                                'set oder list erwartet')

        if gifted is None:
            self._gifted = set()
        else:
            if isinstance(gifted, set):
                self._gifted = gifted
            elif isinstance(gifted, list):
                self._gifted = set(gifted)
            else:
                raise TypeError('`gifted` wird als set oder list erwartet')

    @classmethod
    def load(cls, character,
             directory='C:/Users/49162/Documents/RolePlay/PnP/DSA'):
        """Load character from harddrive and returns corresponding Held object.

        Parameters
        ----------
        character : str
            Name of the character to be loaded. Althogh underscore style is
            used in file naming, the intended name may be used.
        directory : str, optional
            Specifies directory to load <name>.json from.
            The default is 'C:/Users/49162/Documents/RolePlay/PnP/DSA'.

        Raises
        ------
        ValueError
            Raised when specified hero is not found in given directory.

        Returns
        -------
        Hero
            Initiated hero.

        """
        final_file = pathlib.Path(directory,
                                  (character + '.json').replace(' ', '_'))
        if final_file.exists() and final_file.is_file():
            with open(final_file, 'r') as source:
                data = json.load(source)
            return cls._from_json(name=character.replace('_', ' '),
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
            may contain Values for 'incompetences' and 'gifted'.

        Returns
        -------
        hero : Hero
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

    def execute(self, talent, modifier=-0):
        """Perform a test on a certin talent, w.r.t. skikll value and modifier.

        Core functionality.
        This method allow the execution of the dsa signature content: the
        3D20 test. For more details see Held._perform_test or the official
        rules at https://ulisses-regelwiki.de/index.php/GR_Proben.html

        Parameters
        ----------
        talent : str
            State the talent/skill to be tested.
        modifier : int, optional
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
            talent=talent, modifier=modifier,
            attribute_source=self.SKILL_CHECKS)
    
        if impossible:
            msg = ('Die Erschwernis von {} '
                   'macht diese Probe unmöglich.'.format(abs(modifier)))
            return msg

        _3w20 = np.random.randint(1, 21, 3)

        # Zufallsereignis auswerten
        gelungen, krit, qualitätsstufen = self._perform_test(
            aim=objective, random_event=_3w20,
            skill_level=self._skills[talent],
            gifted=(talent in self._gifted),
            incompetent=(talent in self._incompetences))

        # Ausgabe bestimmen
        out = self._format_outcome(
            skill=talent,
            goals=objective,
            random_event=_3w20,
            talent_level=self._skills,
            talent_composition=self.SKILL_CHECKS,
            success=gelungen,
            crit=krit,
            quality_level=qualitätsstufen,
            modification=modifier)
        return out

    def analyze_success(self, talent, modifier=0):        
        """Visualize the probability of the statet test with plot and string.

        Parameters
        ----------
        talent : str
            State the talent/skill to be tested.
        modifier : int, optional
            Modification set to the test; negative values for a more difficult,
            positve values for an easier test
            The default is 0.

        Note
        ----
        As sideeffect a matplotlib panel is displayed within a further process.

        Returns
        -------
        str
            Formatted describtion of quality level distribution for
            specified talent/skill.

        """
        # estimate objectives for rolling
        objective, impossible = self._estimae_objective(
            talent=talent, modifier=modifier,
            attribute_source=self.SKILL_CHECKS)
    
        if impossible:
            msg = ('Die Erschwernis von {} '
                   'macht diese Probe unmöglich.'.format(abs(modifier)))
            return msg

        # generate table with all possible random events
        table = self._n_cartesian_three(20, talent)
        header = list(table.columns)
        qualities = []
        
        # estimate all possible random events
        for index, row in table.iterrows():
            _, _, quality_level = self._perform_test(
                aim=objective,
                random_event=row.to_numpy(),
                skill_level=self._skills[talent],
                gifted=(talent in self._gifted),
                incompetent=(talent in self._incompetences))
            if quality_level == -1:
                quality_level = 0
            qualities.append(quality_level)
        table['#QS'] = qualities

        # begin plotting process
        title='Verteilung der Qualitätsstufen von {}'.format(talent)
        proc = multiprocessing.Process(
            target=plottery.plot_cube_of_success,
            args=(table, title,))
        proc.start()

        # begin describing probabilities
        distribution = ('Erfolgsaussichten für ein Probe auf {} mit '
                        'Modifikator {}:\n\n').format(talent, modifier)

        results = table.groupby('#QS').count().index
        prob = table.groupby('#QS').count()[header[0]].to_numpy(dtype='float')
        prob /= sum(prob)
        
        # following string formating
        delimiter = ' | '
        upper = '     q   ' + delimiter
        lower = ' P(#QS=q)' + delimiter
        for i in range(len(results)):
            if results[i] < 10:
                upper += ('  ' + str(results[i]) + '  ' + delimiter)
            else:
                upper += ('  ' + str(results[i]) + ' ' + delimiter)
            lower += (
                '{:5.2f}'.format(np.round(prob[i]*100, 2))
                + delimiter)
        # correct last char
        upper = upper[:-1]
        lower = lower[:-1]
        line = '-' * len(upper)
        
        distribution += upper + '\n' + line + '\n' + lower + '\n'
        distribution +=  ' '*len(line[:-3]) + '[in Prozent]'

        return distribution

    def update_special_abilities(self, also_permitted=[]):
        """Initiate command line dialogue to update gifted and incompetences.

        After confirmation the corresponding sets are updated.

        Parameters
        ----------
        also_permitted : list, optional
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
                self._gifted)
            if len(temp) > 3:
                raise ValueError('Nicht mehr als 3 Begabungen erlaubt.')
            for t in temp:
                in_skills = t in self.SKILL_CHECKS.keys()
                in_further_skills = t in also_permitted
                if not in_skills and not in_further_skills:
                    raise ValueError('{} ist keine zulässige'
                                     ' Fertigkeit.'.format(t))
            if temp.isdisjoint(self._incompetences):
                self._gifted = temp
            else:
                raise ValueError('Begabungen und Unfähigkeiten'
                                 ' dürfen sich nicht überlappen.')

        # whether inability shall be updated
        val = self._clean_read(text='Unfähigkeiten aktualisieren?\n(j/n) ',
                               legal_response=['j', 'n'])
        if val == 'j':
            temp = self._show_and_update_set(
                '{}\'s Unfähigkeiten:'.format(self.name),
                self._incompetences)
            if len(temp) > 2:
                raise ValueError('Nicht mehr als 2 Unfähigkeiten erlaubt.')
            for t in temp:
                if t not in self.SKILL_CHECKS.keys():
                    raise ValueError('{} ist keine'
                                     ' zulässige Fertigkeit.'.format(t))
            if temp.isdisjoint(self._gifted):
                self._incompetences = temp
            else:
                raise ValueError('Begabungen und Unfähigkeiten'
                                 ' dürfen sich nicht überlappen.')

        val = self._clean_read(
            text='Weitere Aktualisierungen vornehmen?\n(j/n) ',
            legal_response=['j', 'n'])

        # whether more updates shall be happen
        if val == 'j':
            self.update_special_abilities(
                also_permitted=also_permitted)

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
            data_to_dump = {'Eigenschaften': self._attributes,
                            'Fertigkeiten': self._skills,
                            'Begabungen': list(self._gifted),
                            'Unfähigkeiten': list(self._incompetences)}
            with open(pathlib.Path(directory, file),
                      'w') as file:
                json.dump(data_to_dump, file)
        else:
            raise OSError('Mit gültigem Pfad erneut versuchen.'
                          ' Eventuell Schreibrechte überprüfen.')

    def test(self, attribute, modifikator=0):
        """Perform an attribute check, meaning a 1D20 roll.

        Parameters
        ----------
        attribute : str
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
        assert attribute in self._attributes.keys(),\
            '{} ist keine gültige Eigenschaft.'.format(attribute)
        eigenschaftswert_mod = min(
            self._attributes[attribute] + modifikator, 19)
        _1w20 = np.random.randint(1, 21, 1)

        suc, _, _ = self._perform_test(
            aim=np.array(eigenschaftswert_mod),
            random_event=_1w20)

        msg = '{} testet {} ({})'.format(
                self.name, attribute, self._attributes[attribute])
        if modifikator == 0:
            msg += ':\n'
        elif modifikator > 0:
            msg += ', erleichtert um {}:\n'.format(str(abs(modifikator)))
        elif modifikator < 0:
            msg += ', erschwert um {}:\n'.format(str(abs(modifikator)))

        if suc:
            msg += '\nGeschafft mit einem Wurf von {}.'.format(*_1w20)
        else:
            msg += '\nNicht geschafft mit einem Wurf von {}.'.format(*_1w20)

        return msg

    def show_special_abilities(self):
        """Show talents which are marked as gifted or incompetent.

        Returns
        -------
        out : str
            Formatted representation.

        """
        msg_1 = '{}\'s Begabungen:'.format(self.name)
        line = '='*len(msg_1)
        msg_1 += '\n{}\n\t'.format(line)
        for t in self._gifted:
            msg_1 += '{} '.format(t)

        msg_2 = '{}\'s Unfähigkeiten:'.format(self.name)
        line = '='*len(msg_2)
        msg_2 += '\n{}\n\t'.format(line)
        for u in self._incompetences:
            msg_2 += '{} '.format(u)

        out = msg_1 + '\n' + msg_2
        return out

    def show_attributes(self):
        """Show attributes and values.

        Returns
        -------
        str
            Formatted representation.

        """
        return self._show_pretty_dicts(
            '{}\'s Eigenschaften:'.format(self.name), self._attributes)

    def show_skills(self):
        """Show skills and values.

        Returns
        -------
        str
            Formatted representation.

        """
        return self._show_pretty_dicts(
            '{}\'s Fertigkeiten:'.format(self.name), self._skills)

    def get_gifted_skills_gui(self):
        """Getter for gifted skills(`Begabungen`); concerning GUI.

        Returns
        -------
        gifted_skills : list
            List of strings representing the heros' gifted skills.

        """
        gifted_skills = []
        for skill in self._gifted:
            gifted_skills.append(self._tamper_designation(skill))
        return gifted_skills

    def get_incompetent_skills_gui(self):
        """Getter for incompetences(`Unfähigkeiten`); concerning GUI.

        Returns
        -------
        incompetent_skills : list
            List of strings representing the heros' incompetences.

        """
        incompetent_skills = []
        for skill in self._incompetences:
            incompetent_skills.append(self._tamper_designation(skill))
        return incompetent_skills

    def _estimae_objective(self, talent, modifier, attribute_source):
        """Derives objective for random event for a test on talent.
    
        Each talent correspond to three attributes, which values make up the 
        objective to roll against (random event). These values may be modified
        on DM decision, marked by modfier. Each value is lower or equal to 19.
        If any value is lower than one, the test is considered as impossible.
    
        Parameters
        ----------
        talent : str
            skill or spell like to be tested.
        modifier : int
            Alleviation (positive Values) or difficulty on objective.
        attribute_source : dict
            Source to look up attributes for the test of talent. Therefore
            `talent` must be among `attribute_source.keys()`.

        Raises
        ------
        ValueError
            Raised when specified talent is not legal, i.e. is not a key in
            specified `attribute_source`.

        Returns
        -------
        objective : numpy.ndarry
            Estimated objective for test.
        impossible : bool
            Iff any objective value is lower than one after considering the
            modifier.

        """
        try:
            objective = np.array(
                [self._attributes[eig]
                 for eig in attribute_source[talent]])
            add_cap_19 = np.vectorize(
                lambda x: min(19, x + modifier)
                )
            objective = add_cap_19(objective)
        except KeyError:
            raise ValueError('{} ist keine'
                             ' gültige Fertigkeit.'.format(talent))
    
        if any(objective < 1):                  # detect impossible tests
            impossible = True
        else:
            impossible = False
    
        return objective, impossible

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

        if skill in self._gifted:
            kind_of_result = 'Ergebnis der Begabung'
        elif skill in self._incompetences:
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

    def _n_cartesian_three(self, n: int, skill):
        """Generate DataFrame with n**3 rows, corresponding to attributes.

        Parameters
        ----------
        n : int
            One to n describes the base set for cartesian product.
        skill : str
            Designate talent. Must be among keys from self.SKILL_CHECKS.

        Returns
        -------
        out : pandas.DataFrame
            DESCRIPTION.

        """
        base = list(range(1, n+1))
        third = base * (n**2)
        second = []
        first = []
        for e in base:  
            second += [e]*n
            first += [e]*(n**2)
        
        second = second * n
        '[1] ' + self.SKILL_CHECKS[skill][0]
        out = pd.DataFrame({
            '[1] ' + self.SKILL_CHECKS[skill][0]: first,
            '[2] ' + self.SKILL_CHECKS[skill][1]: second,
            '[3] ' + self.SKILL_CHECKS[skill][2]: third})
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
                if key in self._incompetences:
                    msg += ('\n' + key + incomp + ':\n' + '\t'*depth + value)
                elif key in self._gifted:
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


if __name__ == '__main__':
    bob = Hero('Bob', [14]*8, [12]*59)
    df = bob.analyze_success('Zechen')
    print(df)

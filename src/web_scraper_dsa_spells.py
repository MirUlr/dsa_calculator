# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 16:51:22 2022

@author: 49162
"""

import requests
from bs4 import BeautifulSoup

from supernatural_skills import FunzelSkill


def stretch_out(checks: str):
    """`checks` are considered in form 'XX/YY/ZZ'"""
    abbrevations = {
        'MU': 'Mut', 'KL': 'Klugheit', 'IN': 'Intuition',
        'CH': 'Charisma', 'FF': 'Fingerfertigkeit',
        'GE': 'Gewandtheit', 'KO': 'Konstitution', 'KK': 'Körperkraft'
        }
    out = [abbrevations[key[:2]] for key in checks.split(sep='/')]
    
    designation = ['erstes_Attribut', 'zweites_Attribut', 'drittes_Attribut']
    
    return designation, out
    

url = 'https://ulisses-regelwiki.de/zauberauswahl.html'
sub_url = 'https://ulisses-regelwiki.de/'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='main')

links_to_spells = results.find_all('a')

spells = set()
for link in links_to_spells:
    temp = sub_url + link['href']
    spell_page = requests.get(temp)
    
    spell_soup = BeautifulSoup(spell_page.content, 'html.parser')
    result = spell_soup.find(id='main')

    temp = dict()
    temp['name'] = result.find('div', class_='header').text.strip()
    body = result.find('div', class_='body')
    
    fields = body.find_all('div')
    for idx, field in enumerate(fields):
        if idx == 13:
            break

        if idx % 2 == 0:
            if field.text.strip().endswith('Kosten:'):
                temp['kosten'] = fields[idx+1].text.strip()
            elif field.text.strip() != 'Probe:':
                temp[field.text.strip().replace(':', '').lower()] =\
                    fields[idx+1].text.strip()
            elif field.text.strip() == 'Probe:':
                key, vals = stretch_out(fields[idx+1].text.strip())
                for k, v in zip(key, vals):
                    temp[k.lower()] = v
            else:
                raise RuntimeError()
                
    spells.add(FunzelSkill(**temp))
    
    if len(spells) % 20 == 0:
        print(f'Scraped {len(spells)} spells; work is going on ...')

print()
for spell in spells:
    print(spell)

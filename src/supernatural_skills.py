# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 18:51:17 2022

@author: 49162
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FunzelSkill:
    name: str = field(repr=True)
    erstes_attribut: str = field(repr=True)
    zweites_attribut: str = field(repr=True)
    drittes_attribut: str = field(repr=True)
    wirkung: str = field(repr=False)
    zauberdauer: str = field(repr=True)
    kosten: str = field(repr=True)
    reichweite: str = field(repr=False)
    wirkungsdauer: str = field(repr=False)
    zielkategorie: str = field(repr=False)

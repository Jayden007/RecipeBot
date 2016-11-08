# coding: utf-8
from __future__ import unicode_literals
from INTENTS import getWeather, entities


def botEngine(text):
    
    _, ent = entities.disintegrate(text,['DATE'])
    getWeather.getWeather(ent)
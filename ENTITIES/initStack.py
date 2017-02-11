#coding: utf-8
from __future__ import unicode_literals
import pickle
import os

Smemory = {'prompt': False, 'DATE' : 0, 'LOCATION' : None}

print os.getcwd()

f = open("ENTITIES/stack.txt", 'wb')
pickle.dump(Smemory, f, protocol=0)
f.close()
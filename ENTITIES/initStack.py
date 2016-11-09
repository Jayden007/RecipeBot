#coding: utf-8
from __future__ import unicode_literals
import pickle

Smemory = {'prompt': False, 'DATE' : 0, 'LOCATION' : None}

f = open("stack.txt", 'wb')
pickle.dump(Smemory, f, protocol=0)
f.close()
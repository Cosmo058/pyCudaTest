import itertools
import time
import unicodedata
import pycuda.driver as cuda
import hashlib
import numpy


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', unicode(s, "ISO-8859-1")).encode("ascii", "ignore"))


NumLetras = 7

permutaciones = list(itertools.permutations(list('rotzszriefuc'), NumLetras))
NumPerm = len(permutaciones)
print "Hay " + str(NumPerm) + " posibles combinaciones"

if NumLetras == 8:
    resultado = [x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] + x[7] for x in permutaciones]
if NumLetras == 7:
    resultado = [x[0] + x[1] + x[2] + x[3] + x[4] + x[5] + x[6] for x in permutaciones]
if NumLetras == 6:
    resultado = [x[0] + x[1] + x[2] + x[3] + x[4] + x[5] for x in permutaciones]
if NumLetras == 5:
    resultado = [x[0] + x[1] + x[2] + x[3] + x[4] for x in permutaciones]
if NumLetras == 4:
    resultado = [x[0] + x[1] + x[2] + x[3] for x in permutaciones]
if NumLetras == 3:
    resultado = [x[0] + x[1] + x[2] for x in permutaciones]

del permutaciones

for idx, palabra in enumerate(resultado):
    hash_object = hashlib.md5(palabra)
    resultado[idx] = hash_object.hexdigest()


def make_dict():
    d = []
    with open("es.dic", "r") as wordfile:
        for word in wordfile:
            word = strip_accents(word.strip().lower())
            if len(word) == NumLetras:
                # d.append(word)
                hash_object = hashlib.md5(word)
                d.append(hash_object.hexdigest())
        print "Diccionario de tamano " + str(len(d))
    return d


d = make_dict()
diccionario = numpy.array(d)
pal = []

for indice in range(0, NumPerm):
    if indice % 1000 == 0: print "I: " + str(indice) + "    F:" + str(len(pal)) + "    P: " + str((indice / float(NumPerm) * 100)) + "%".join(pal)
    if resultado[indice] in d:
        if resultado[indice] not in pal:
            pal.append(resultado[indice])

print "\n".join(pal)
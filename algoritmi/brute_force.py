import numpy as np
from itertools import permutations
from statistika.statistika_algoritma import Statistika


class BruteForce:
    def __init__(self, evaluator):
        self._statisika = Statistika()
        self._evaluator = evaluator
        self._broj_gradova = evaluator.get_broj_gradova()

    def izracunaj_najkraci_put(self):
        self._statisika.pocetak()
        any(self._izracunaj_put(put) for put in permutations(np.arange(self._broj_gradova)))
        self._statisika.kraj()
        return self._statisika.get_statistiku()

    def _izracunaj_put(self, put):
        duljina_puta = self._evaluator.izracunaj_duljinu_puta(np.array(put).reshape(1, -1))[0]
        self._statisika.update((put, duljina_puta))

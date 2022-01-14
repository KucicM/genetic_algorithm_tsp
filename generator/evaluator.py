import numpy as np


class Evaluator:
    def __init__(self, matica_udaljenost):
        self._matica_udaljenost = matica_udaljenost

    def izracunaj_duljinu_puta(self, put):
        # put moze biti 1d ili 2d matirca, u 2d matrici redak je put
        return np.sum(self._matica_udaljenost[np.roll(put, 1, axis=1), put], axis=1)

    def get_broj_gradova(self):
        return self._matica_udaljenost.shape[0]
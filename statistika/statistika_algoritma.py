from time import time
from numpy import inf


class Statistika:
    def __init__(self):
        self._statistika = {'put': None, 'duljina_puta': inf}

    def pocetak(self):
        self._statistika['vrijeme'] = time()

    def update(self, put_duljina):
        put, duljina_puta = put_duljina
        if duljina_puta < self._statistika['duljina_puta']:
            self._statistika['put'], self._statistika['duljina_puta'] = put, duljina_puta
            return True
        return False

    def kraj(self):
        self._statistika['ukupno_vrijeme'] = time() - self._statistika['vrijeme']

    def get_statistiku(self):
        return self._statistika

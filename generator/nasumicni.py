import numpy as np
from generator.evaluator import Evaluator


class NasumicniGradovi:
    '''
    sluzi za generiranje gradova u 2d na nasumicnim pozicijama.
    Ako se definira broj gradova, gradovi ce se generirati, ako je broj_gradova=None, 
    tada ce se pokusati ucitati koordinate gradova iz dane putanje.
    '''
    def __init__(self, broj_gradova, putanja=None, ime_fila=None):
        assert not (broj_gradova is None and putanja is None and ime_fila is None),\
            'mora se definirati ili broj_gradova ili putanja'

        if putanja is not None and ime_fila is not None:
            self._putanja_ime = putanja + ime_fila
        else:
            self._putanja_ime = None

        if broj_gradova is None: # Ucitavanje koordinata
            assert self._putanja_ime, 'putanja ili ime_fila su None'
            self._ucitaj_kooridnate()
        else:
            self._br_gradova = int(broj_gradova)
            assert self._br_gradova > 0, 'Broj gradova mora biti veci od 0'
            self._generiraj_gradove()

    def _generiraj_gradove(self):
        self._koordinate = (self._generiraj_kooridinate() + 1j * self._generiraj_kooridinate()).reshape(-1, 1)
        self._izracunaj_matricu_udaljenosti()
        self._evaulator = Evaluator(self._udaljenosti)

        if self._putanja_ime is not None:
            self._spremi_koordinate()

    def get_evaluator(self):
        return self._evaulator

    def get_koordinate(self):
        return self._koordinate

    def get_matricu_udaljenosti(self):
        return self._udaljenosti

    def _generiraj_kooridinate(self):
        return np.random.choice(self._br_gradova, size=self._br_gradova, replace=False)

    def _izracunaj_matricu_udaljenosti(self):
        diff = self._koordinate.T - self._koordinate # nije 'conjugate transpose'
        self._udaljenosti = np.sqrt(np.real(diff)**2 + np.imag(diff)**2)

    def _spremi_koordinate(self):
        np.save(self._putanja_ime, self._koordinate)

    def _ucitaj_kooridnate(self):
        self._koordinate = np.load(self._putanja_ime)
        self._izracunaj_matricu_udaljenosti()
        self._evaulator = Evaluator(self._udaljenosti)

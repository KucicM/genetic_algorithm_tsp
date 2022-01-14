import numpy as np
from generator.evaluator import Evaluator


class GradoviNaKruznici:
    '''
    generira gradove na kruznici radiusa 1
    '''
    def __init__(self, broj_gradova):
        self._br_gradova = int(broj_gradova)
        assert self._br_gradova > 0, 'Broj gradova mora biti veci od 0'
        self._generiraj_gradove()

    def _generiraj_gradove(self):
        self._koordinate = np.exp(1j * np.linspace(0, 2*np.pi, self._br_gradova+1)).reshape(-1, 1)
        self._izracunaj_matricu_udaljenosti()
        self._evaulator = Evaluator(self._udaljenosti)

    def _izracunaj_matricu_udaljenosti(self):
        diff = self._koordinate.T - self._koordinate # nije 'conjugate transpose'
        self._udaljenosti = np.sqrt(np.real(diff)**2 + np.imag(diff)**2)

    def get_evaluator(self):
        return self._evaulator

    def get_koordinate(self):
        return self._koordinate

    def get_matricu_udaljenosti(self):
        return self._udaljenosti

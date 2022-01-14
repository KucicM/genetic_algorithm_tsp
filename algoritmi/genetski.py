import numpy as np
from statistika.statistika_algoritma import Statistika


class GenetskiAlgoritam:
    def __init__(self, velicina_populacije, vjerojatnost_mutiranja, vjerojatnost_krizanja, evaluator):

        velicina_populacije = int(velicina_populacije)
        assert velicina_populacije > 0, 'populacija mora biti veca od 0'
        self._velicina_populacije = velicina_populacije

        vjerojatnost_mutiranja = float(vjerojatnost_mutiranja)
        assert 0 <= vjerojatnost_mutiranja <= 1, 'vjerojatnost_mutiranja mora biti izmedju 0 i 1'
        self._vjerojatnost_mutiranja = vjerojatnost_mutiranja

        vjerojatnost_krizanja = float(vjerojatnost_krizanja)
        assert 0 <= vjerojatnost_krizanja <= 1, 'vjerojatnost_krizanja mora biti izmedju 0 i 1'
        self._vjerojatnost_krizanja = vjerojatnost_krizanja

        assert evaluator is not None, 'evaluator ne moze biti None'
        self._br_gradova = evaluator.get_broj_gradova()
        self._evaluacija_populacije = evaluator

        self._populacija = None
        self._statistika = Statistika()


    def izracunaj_najkraci_put(self, br_generacija_bez_promijene=100):
        bez_promjene = 0
        self._statistika.pocetak()
        while bez_promjene < br_generacija_bez_promijene:
            promjena = self._jedna_generacija()
            bez_promjene = 0 if promjena else bez_promjene + 1

        self._statistika.kraj()
        return self._statistika.get_statistiku()

    def _jedna_generacija(self):
        if self._populacija is None:
            self._init_populacije()

        # evaluacija trenutne generacije
        fitnes = self._izracunaj_fitnes()
        norm_fitnes = self._normalizirani_fitnes(fitnes)

        # najbolji u generaciji
        idx_najbolje_jedinke = np.argmax(norm_fitnes)
        najkraci_put = self._populacija[idx_najbolje_jedinke, :].copy()
        najkraca_udaljenost = 1 / fitnes[idx_najbolje_jedinke]

        # priprema iduce generacije
        self._selekcija_nove_populacije(norm_fitnes)
        self._krizanje()
        self._mutiranje()

        return self._statistika.update((najkraci_put, najkraca_udaljenost))

    def _init_populacije(self):
        populacije_idx = np.argsort(
            np.random.rand(self._br_gradova, self._velicina_populacije),
            axis=0)
        self._populacija = np.arange(self._br_gradova)[populacije_idx].T

    def _izracunaj_fitnes(self):
        return 1 / self._evaluacija_populacije.izracunaj_duljinu_puta(self._populacija)

    def _normalizirani_fitnes(self, fitnes):
        return fitnes / np.sum(fitnes)

    def _selekcija_nove_populacije(self, norm_fitnes):
        idxs = np.random.choice(self._velicina_populacije, size=self._velicina_populacije, p=norm_fitnes)
        self._populacija = self._populacija[idxs, :]

    def _mutiranje(self):
        jedinke = self._generiraj_nasumicni_uzorak_jedinki(self._vjerojatnost_mutiranja)
        if len(jedinke) == 0:
            return

        gradovi = np.random.randint(0, self._populacija.shape[1], size=(self._populacija.shape[0], 2))
        self._populacija[(jedinke, jedinke), (gradovi[jedinke, 0], gradovi[jedinke, 1])] =\
            self._populacija[(jedinke, jedinke), (gradovi[jedinke, 1], gradovi[jedinke, 0])]

    def _krizanje(self):
        jedinke = self._generiraj_nasumicni_uzorak_jedinki(self._vjerojatnost_krizanja)
        if len(jedinke) == 0:
            return

        self._populacija[jedinke] = np.apply_along_axis(self._merge, 1, self._stack(jedinke))

    def _stack(self, jedinke):
        pocetni_idx = np.random.choice(self._populacija.shape[1])
        return np.hstack((self._populacija[jedinke][:, pocetni_idx:], np.roll(self._populacija[jedinke], 1, axis=0)))

    def _merge(self, redak):
        return redak[np.sort((np.unique(redak, return_index=True)[1]), kind='heapsort')]


    def _generiraj_nasumicni_uzorak_jedinki(self, vjerojatnost_odabira):
        return np.nonzero(np.random.rand(self._velicina_populacije) < vjerojatnost_odabira)[0]

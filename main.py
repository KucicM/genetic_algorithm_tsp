import pomocni
import logging

from vizualizacija import plot
from generator import pomocni as gen
from generator.nasumicni import NasumicniGradovi
from generator.kruzni import GradoviNaKruznici
from algoritmi import pomocni as algos
from konstante import postavke, imena


PLOT = False

#### POKRETANJE IZ TERMINALA ######
if __name__ == '__main__':

    pomocni.set_logger(False)
    pomocni.ispis_verzija_koristenih_modula()
    pomocni.init_putanje()

    # ISPITIVANJE BF ALGORITMA
    nasumicni_args = gen.get_args_nasumicnih_gradova(postavke.MANJI_BROJ_GRADOVA)
    nasumicni_evaulatori = gen.generiranje_gradova(NasumicniGradovi, nasumicni_args)
    algos.ispitivanje_bf_algoritma(
        nasumicni_evaulatori,
        postavke.BROJ_ITERACIJA,
        imena.BF_FILE_VAR_BR_GRADOVA
    )

    if PLOT:
        plot.prikaz_bf_vs_br_gradova(imena.PUTANJA_REZULTATA, imena.BF_FILE_VAR_BR_GRADOVA)

    #### Ispitivanje ####

    ## Manji broj gradova (nasumicno) ##
    nasumicni_args = gen.get_args_nasumicnih_gradova(postavke.MANJI_BROJ_GRADOVA, ucitavanje=True)
    nasumicni_evaulatori = gen.generiranje_gradova(NasumicniGradovi, nasumicni_args)

    algos.ispitivanje_ga_algoritma(
        nasumicni_evaulatori,
        postavke.BROJ_ITERACIJA,
        postavke.MANJI_BROJ_JEDINKI,
        postavke.VJEROJATNOSTI_MUTACIJE,
        postavke.VJEROJATNOSIT_KRIZANJA,
        imena.GA_FILE_MANJI_BR_GRADOVA
    )

    if PLOT:
        plot.prikaz_ga_vs_ref(
            imena.PUTANJA_REZULTATA,
            imena.BF_FILE_VAR_BR_GRADOVA,
            imena.GA_FILE_MANJI_BR_GRADOVA
        )

    ## Veci broj gradova ##
    kruzni_args = gen.get_args_kruznih_gradova(postavke.VECI_BROJ_GRADOVA)
    kruzni_evaulatori = gen.generiranje_gradova(GradoviNaKruznici, kruzni_args)
    
    algos.ispitivanje_kruznih_gradova(kruzni_evaulatori, imena.REF_FILE_VAR_BR_GRADOVA_VECI)
    algos.ispitivanje_ga_algoritma(
        kruzni_evaulatori,
        postavke.BROJ_ITERACIJA,
        postavke.VECI_BROJ_JEDINKI,
        postavke.VJEROJATNOSTI_MUTACIJE,
        postavke.VJEROJATNOSIT_KRIZANJA,
        imena.GA_FILE_VECI_BR_GRADOVA
    )

    if PLOT:
        plot.prikaz_ga_vs_ref(
            imena.PUTANJA_REZULTATA,
            imena.REF_FILE_VAR_BR_GRADOVA_VECI,
            imena.GA_FILE_VECI_BR_GRADOVA
        )

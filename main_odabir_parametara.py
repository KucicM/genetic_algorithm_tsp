import pomocni
from generator import pomocni as gen
from konstante import postavke, imena
from generator.nasumicni import NasumicniGradovi
from algoritmi import pomocni as algos
from vizualizacija import plot


PLOT = False

if __name__ == '__main__':

    pomocni.set_logger(False)
    pomocni.ispis_verzija_koristenih_modula()
    pomocni.init_putanje()


    ###### Odabir parametara algoritma #######
    postavka_nasumicnog_evaluatora = gen.get_args_nasumicnih_gradova(postavke.KONSTANTAN_BROJ_GRADOVA)
    nasumicni_evaulatori = gen.generiranje_gradova(NasumicniGradovi, postavka_nasumicnog_evaluatora)

    ######## 1. Odabir vjerojatnosti mutiranja i križanja #######
    algos.ispitivanje_ga_algoritma(
        nasumicni_evaulatori,
        postavke.BROJ_ITERACIJA,
        postavke.KONSTANTAN_BROJ_JEDINKI,
        postavke.VARIJACIJA_VJV_MUTACIJE,
        postavke.VARIJACIJA_VJV_KRIZANJA,
        imena.GA_FILE_VAR_VJV
    )

    if PLOT:
        plot.prikaz_varijacija(imena.PUTANJA_REZULTATA, imena.GA_FILE_VAR_VJV)

    ######## 2. Odabir broja jedinki (veličine populacije) ##########

    ### Vjerojatnosti = 0 ###
    algos.ispitivanje_ga_algoritma(
        nasumicni_evaulatori,
        postavke.BROJ_ITERACIJA,
        postavke.VARIJACIJA_BROJA_JEDINKI,
        postavke.VJEROJATNOSTI_MUTACIJE_0,
        postavke.VJEROJATNOSIT_KRIZANJA_0,
        imena.GA_FILE_VAR_POP_VJV_0
    )

    if PLOT:
        plot.prikaz_ga_vs_br_jedinki(imena.PUTANJA_REZULTATA, imena.GA_FILE_VAR_POP_VJV_0)

    postavka_nasumicnog_evaluatora = gen.get_args_nasumicnih_gradova(postavke.KONSTANTAN_BROJ_GRADOVA, ucitavanje=True)
    nasumicni_evaulatori = gen.generiranje_gradova(NasumicniGradovi, postavka_nasumicnog_evaluatora)

    ### Vjerojatnosti != 0 ###
    algos.ispitivanje_ga_algoritma(
        nasumicni_evaulatori,
        postavke.BROJ_ITERACIJA,
        postavke.VARIJACIJA_BROJA_JEDINKI,
        postavke.VJEROJATNOSTI_MUTACIJE,
        postavke.VJEROJATNOSIT_KRIZANJA,
        imena.GA_FILE_VAR_POP
    )

    if PLOT:
        plot.prikaz_ga_vs_br_jedinki(imena.PUTANJA_REZULTATA, imena.GA_FILE_VAR_POP)

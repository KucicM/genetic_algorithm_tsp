import logging
import pandas as pd
import numpy as np
from algoritmi.brute_force import BruteForce
from algoritmi.genetski import GenetskiAlgoritam
from argumenti import get_brute_force_args, get_kruzni_args, get_ga_args, get_rezultati_insert
from konstante import imena
from itertools import product


def ispitivanje_bf_algoritma(evaluatori, broj_iteracija, ime_fila):
    rezultati = []
    for evaluator in evaluatori:
        logging.debug('Ispitivanje brute force algoritma s {} gradova'.format(evaluator.get_broj_gradova()))
        rezultati.extend(ispitivanje(BruteForce, get_brute_force_args(evaluator), broj_iteracija))
    spremi_rezultate(rezultati, ime_fila)


def ispitivanje_kruznih_gradova(evaluatori, ime_fila):
    rezultati = []
    for evaluator in evaluatori:
        duljina_puta = evaluator.izracunaj_duljinu_puta(np.arange(evaluator.get_broj_gradova()).reshape(1, -1))[0]
        rezultati.append(get_kruzni_args(evaluator.get_broj_gradova(), duljina_puta))
    spremi_rezultate(rezultati, ime_fila)


def ispitivanje_ga_algoritma(evaluatori, broj_iteracija,
        populacije, mutacije, krizanja, ime_fila):

    evaluatori = evaluatori if type(evaluatori) is list else [evaluatori]
    populacije = populacije if type(populacije) is list else [populacije]
    mutacije = mutacije if type(mutacije) is list else [mutacije]
    krizanja = krizanja if type(krizanja) is list else [krizanja]

    rezultati = []
    for evaluator, pop, mut, kriz in product(evaluatori, populacije, mutacije, krizanja):
        logging.info(
            'Ispitivanje genetskog algoritma s {} gradova; populacija: {}; vjv_mutacije: {:.3f}; vjv_krizanja: {:.3f};'
            .format(evaluator.get_broj_gradova(), int(pop), float(mut), float(kriz)))

        postavke_algoritma = get_ga_args(pop, mut, kriz, evaluator)

        rez = ispitivanje(GenetskiAlgoritam, postavke_algoritma, broj_iteracija, 50)

        del postavke_algoritma['evaluator']
        rezultati.extend([{**r, **postavke_algoritma} for r in rez])

    spremi_rezultate(rezultati, ime_fila)


def ispitivanje(algoritam, args, broj_iteracija, br_generacija_bez_promijene=None):
    logging.debug('Algoritam {} s argumentima {}'.format(algoritam.__name__, args))
    broj_gradova = args['evaluator'].get_broj_gradova()
    
    rezultati = []
    for i in range(broj_iteracija):
        algo = algoritam(**args)

        if br_generacija_bez_promijene is None:
            rez = algo.izracunaj_najkraci_put()
        else:
            rez = algo.izracunaj_najkraci_put(br_generacija_bez_promijene)

        rezultati.append(get_rezultati_insert(broj_gradova, rez['duljina_puta'], rez['ukupno_vrijeme'], i))

    logging.info('{} broj gradova {} iteracija {} ukupno vrijeme {:.4f}'
        .format(algoritam.__name__, broj_gradova,
            broj_iteracija, np.sum([d['vrijeme'] for d in rezultati]))
    )

    return rezultati


###### SPREMANJE PODATAKA ########
def spremi_rezultate(rezultati, ime):
    df = pd.DataFrame(rezultati)
    putanja_spremanja = imena.PUTANJA_REZULTATA + ime
    logging.info('Spremanje rezultata {}'.format(putanja_spremanja))
    df.to_csv(putanja_spremanja,
        sep='|',
        header=True,
        index=False,
        compression='gzip'
    )

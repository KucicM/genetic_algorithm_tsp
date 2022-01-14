def get_nasumicni_args(broj_gradova, putanja, ime_fila):
    return {'broj_gradova': broj_gradova, 'putanja': putanja, 'ime_fila': ime_fila}


def get_brute_force_args(evaluator):
    return {'evaluator': evaluator}


def get_kruzni_args(broj_gradova, duljina_puta=None):
    if duljina_puta is None: 
        return {'broj_gradova': broj_gradova}
    else: 
        return {'broj_gradova': broj_gradova, 'duljina_puta': duljina_puta}


def get_ga_args(pop, mut, kriz, evaluator):
    return {'velicina_populacije': pop, 'vjerojatnost_mutiranja': mut,
        'vjerojatnost_krizanja': kriz, 'evaluator': evaluator}


def get_rezultati_insert(broj_gradova, duljina_puta, vrijeme, iteracija):
    return {'broj_gradova': broj_gradova, 'duljina_puta': duljina_puta,
        'vrijeme': vrijeme, 'iteracija': iteracija}
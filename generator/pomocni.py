from konstante import imena
from argumenti import get_nasumicni_args, get_kruzni_args


def get_args_nasumicnih_gradova(brojevi_gradova, ucitavanje=False):
    assert brojevi_gradova is not None, 'brojevi_gradova mora biti not None'
    brojevi_gradova = brojevi_gradova if type(brojevi_gradova) is list else [brojevi_gradova]
    ret = []
    for br in brojevi_gradova:
        ret.append(get_nasumicni_args(
            None if ucitavanje else br,
            imena.PUTANJA_POSTAVKA,
            'nasumicni_{}.npy'.format(br))
        )
    return ret


def get_args_kruznih_gradova(brojevi_gradova):
    assert brojevi_gradova is not None, 'brojevi_gradova mora biti not None'
    brojevi_gradova = brojevi_gradova if type(brojevi_gradova) is list else list(brojevi_gradova)
    return [get_kruzni_args(br) for br in brojevi_gradova]


def generiranje_gradova(algo, args):
    return [algo(**arg).get_evaluator() for arg in args]

import os
import logging
from konstante import imena


def ispis_verzija_koristenih_modula():
    logging.info('Korištene verzije modula su:')
    from platform import python_version
    logging.info('Python verzija: {}'.format(python_version()))
    from numpy.version import version
    logging.info('Numpy verzija: {}'.format(version))
    from pandas import __version__
    logging.info('Pandas verzija: {}'.format(__version__))
    from matplotlib import __version__
    logging.info('Matplotlib verzija: {}'.format(__version__))
    from seaborn import __version__
    logging.info('Seaborn verzija: {}'.format(__version__))


def mkdir(putanja):
    if not os.path.isdir(putanja):
        os.mkdir(putanja)


def init_putanje():
    mkdir(imena.PUTANJA_REZULTATA)
    mkdir(imena.PUTANJA_POSTAVKA)


def set_logger(debug=False):
    if debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("./logs/{}.log".format(imena.TEST_IDX)),
                logging.StreamHandler()
            ]
        )
    else: # npr iz jupytera
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[logging.StreamHandler()]
        )

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.titlesize'] = 16


def prikaz_gradova(generator):
    fig, axs = plt.subplots(1, 2, figsize=(20, 5))
    koordinate = generator.get_koordinate()
    axs[0].scatter(np.real(koordinate), np.imag(koordinate), s=100)
    axs[0].set_title('Pozicije gradova na karti')
    axs[0].grid()

    sns.heatmap(generator.get_matricu_udaljenosti(), ax=axs[1]);
    axs[1].set_title('Matrica udaljenosti')
    axs[1].set_ylabel('Odredište')
    axs[1].set_xlabel('Polazište')
    plt.yticks(rotation=0) 
    plt.show();


def get_podaci(putanja, file):
    return pd.read_csv(putanja + file, compression='gzip', delimiter='|')


def ucitavanje_podataka(f):
    def podaci(putanja, file):
        return f(get_podaci(putanja, file))
    return podaci


@ucitavanje_podataka
def prikaz_bf_vs_br_gradova(df):
    df = df.groupby(['broj_gradova'])['vrijeme', 'duljina_puta'].median()
    fig, axs = plt.subplots(figsize=(20, 5))
    axs.plot(df['vrijeme'])
    axs.set_title('Vrijeme ispitivanje svih kombinacija za zadani broj gradova')
    axs.set_xlabel('Broj gradova')
    axs.set_ylabel('Vrijeme [s]')
    plt.grid()
    plt.show();


@ucitavanje_podataka
def prikaz_varijacija(df):
    df = df.groupby(['vjerojatnost_krizanja', 'vjerojatnost_mutiranja'])['vrijeme', 'duljina_puta'].median()

    fig, axs = plt.subplots(1, 2, figsize=(20, 5))
    
    axs[0].set_title('Vrijeme')
    sns.heatmap(df.unstack()['vrijeme'].round(3), ax=axs[0])
    axs[0].set_xticklabels(['{:.2f}'.format(float(t.get_text())) for t in axs[0].get_xticklabels()])
    axs[0].set_yticklabels(['{:.2f}'.format(float(t.get_text())) for t in axs[0].get_yticklabels()])
    axs[0].tick_params(rotation=0)

    axs[1].set_title('Duljina puta')
    sns.heatmap(df.unstack()['duljina_puta'].round(3), ax=axs[1])
    axs[1].set_xticklabels(['{:.2f}'.format(float(t.get_text())) for t in axs[1].get_xticklabels()])
    axs[1].set_yticklabels(['{:.2f}'.format(float(t.get_text())) for t in axs[1].get_yticklabels()])
    plt.gcf().subplots_adjust(bottom=0.15)
    axs[1].tick_params(rotation=0)
    plt.show();



@ucitavanje_podataka
def prikaz_ga_vs_br_jedinki(df):
    df = df.groupby(['velicina_populacije'])['vrijeme', 'duljina_puta'].median()
    fig, axs = plt.subplots(figsize=(20, 5))
    axs.plot(df['vrijeme'])
    axs.set_title('Vrijeme za GA')
    axs.set_xlabel('Veličina populacije')
    axs.set_ylabel('Vrijeme [s]')
    plt.grid()
    plt.show();


def prikaz_ga_vs_ref(putanja, ref_ime, ga_ime):
    ref_df = get_podaci(putanja, ref_ime)
    vrijeme = 'vrijeme' in ref_df.columns
    if vrijeme:
        ref_df = ref_df.groupby(['broj_gradova'])['vrijeme', 'duljina_puta'].median()
    else:
        ref_df = ref_df.groupby(['broj_gradova'])['duljina_puta'].median()

    ga_df = get_podaci(putanja, ga_ime)
    ga_df = ga_df.groupby(['broj_gradova', 'velicina_populacije'])['vrijeme', 'duljina_puta'].median()

    fig, axs = plt.subplots(1, 2, figsize=(20, 5))

    if vrijeme:
        unstack = ga_df.unstack()
        axs[0].plot(unstack['vrijeme'], label='GA')
        axs[0].plot(ref_df['vrijeme'], label='Sve kombinacije')
        axs[0].set_title('Vrijeme GA i ispitivanje svih kombinacija')
        axs[0].set_xlabel('Broj gradova')
        axs[0].set_ylabel('Vrijeme [s]')
        axs[0].legend()
        axs[0].grid()
        res = (unstack['duljina_puta'][unstack['duljina_puta'].columns[0]] / ref_df['duljina_puta'] - 1) * 100
        axs[1].plot(res)
    else:
        unstack = ga_df.unstack()
        for col in unstack['vrijeme'].columns:
            axs[0].plot(unstack['vrijeme'][col], label='populacija {}'.format(col))

        axs[0].set_title('Vrijeme GA')
        axs[0].set_xlabel('Broj gradova')
        axs[0].set_ylabel('Vrijeme [s]')
        axs[0].grid()
        axs[0].legend()
    
        for col in unstack['duljina_puta'].columns:
            res = (unstack['duljina_puta'][col] / ref_df - 1) * 100
            axs[1].plot(res, label='populacija {}'.format(col))
        axs[1].legend()

    axs[1].set_title('Greška GA')
    axs[1].set_xlabel('Broj gradova')
    axs[1].set_ylabel('Razlika duljine obilaska [%]')
    axs[1].grid()
    plt.show();

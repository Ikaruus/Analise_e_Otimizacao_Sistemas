"""Gráficos: pip install matplotlib; execute na pasta codigo.

python gerar_graficos.py --dados ../resultados --graficos ../graficos
"""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CORES = {
    'fib_original': '#d35f53',
    'fib_memoizado': '#278c93',
}
NOMES = {
    'fib_original': 'Original recursivo',
    'fib_memoizado': 'Memoização (AV2)',
}


def ler(caminho):
    with caminho.open(encoding='utf-8', newline='') as arquivo:
        retorno = list(csv.DictReader(arquivo))
    return [{'n': int(l['n']), 'algoritmo': l['algoritmo'],
             'tempo_ms': float(l['mediana_s']) * 1000} for l in retorno]


def setup():
    plt.rcParams.update({'figure.facecolor': 'white', 'axes.facecolor': 'white',
                         'axes.edgecolor': '#c9d2dc', 'axes.labelcolor': '#24364d',
                         'axes.titleweight': 'bold', 'font.size': 11,
                         'grid.color': '#e3eaf1', 'grid.alpha': .9})


def comparacao(dados, arquivo, titulo, selecao):
    fig, ax = plt.subplots(figsize=(9.5, 4.7))
    for alg in selecao:
        linhas = sorted([l for l in dados if l['algoritmo'] == alg], key=lambda x:x['n'])
        ax.plot([l['n'] for l in linhas], [l['tempo_ms'] for l in linhas],
                'o-', lw=2.5, ms=6, label=NOMES[alg], color=CORES[alg])
    ax.set_yscale('log')
    ax.set_title(titulo, loc='left', fontsize=15, pad=17)
    ax.set_xlabel('Índice de Fibonacci (n)')
    ax.set_ylabel('Tempo por chamada (ms, escala logarítmica)')
    ax.grid(True, which='major', axis='y')
    ax.legend(frameon=False, loc='upper left')
    ax.text(.01, -.20, 'Fonte: benchmark executado neste ambiente; mediana de 7 rodadas.',
            transform=ax.transAxes, color='#697c90', fontsize=9)
    fig.tight_layout()
    fig.savefig(arquivo, dpi=190, bbox_inches='tight')
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dados', type=Path, default=Path('resultados'))
    parser.add_argument('--graficos', type=Path, default=Path('graficos'))
    args = parser.parse_args()
    args.graficos.mkdir(parents=True, exist_ok=True)
    setup()
    if (args.dados/'av2_comparacao.csv').exists():
        comparacao(ler(args.dados/'av2_comparacao.csv'), args.graficos/'av2_tempos.png',
                   'AV2 | Antes e depois da memoização', ['fib_original','fib_memoizado'])
    print('Gráficos salvos em', args.graficos.resolve())


if __name__ == '__main__':
    main()

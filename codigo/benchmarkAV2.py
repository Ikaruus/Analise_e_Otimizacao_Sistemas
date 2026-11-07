"""AV2: original versus primeira otimização, para entradas equivalentes."""
import argparse
from pathlib import Path
from algoritmos import fib_original, fib_memoizado
from medicao import medir, salvar_csv, registrar_ambiente


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--saida', type=Path, default=Path('resultados'))
    parser.add_argument('--repeticoes', type=int, default=7)
    args = parser.parse_args()
    entradas = [10, 15, 20, 25, 28, 30, 32]
    linhas = []
    for n in entradas:
        assert fib_original(n) == fib_memoizado(n)
        for funcao in (fib_original, fib_memoizado):
            item = medir(funcao, n, args.repeticoes)
            linhas.append(item)
            print(f"n={n:>2}  {item['algoritmo']:<17}  mediana={item['mediana_s']:.9f} s")
    salvar_csv(args.saida / 'av2_comparacao.csv', linhas)
    registrar_ambiente(args.saida / 'ambiente.txt')
    print('Arquivos salvos em', args.saida.resolve())


if __name__ == '__main__':
    main()

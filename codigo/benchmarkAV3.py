"AV3: comparação das três versões e escabilidade das otimizações."
import argparse
from pathlib import Path
from algoritmos import fib_original, fib_memoizado, fib_iterativo
from medicao import medir, salvar_csv, registrar_ambiente


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--saida', type=Path, default=Path('resultados'))
    parser.add_argument('--repeticoes', type=int, default=7)
    args = parser.parse_args()
    comparacao, escalabilidade = [], []
    for n in [10, 15, 20, 25, 28, 30, 32]:
        assert fib_original(n) == fib_memoizado(n) == fib_iterativo(n)
        for funcao in (fib_original, fib_memoizado, fib_iterativo):
            item = medir(funcao, n, args.repeticoes)
            comparacao.append(item)
            print(f"Comparação: n={n:>2}  {item['algoritmo']:<17}  mediana={item['mediana_s']:.9f} s")

    # Memoização recursiva tem limite de pilha; usar apenas entradas moderadas.
    for n in [50, 100, 200, 300]:
        assert fib_memoizado(n) == fib_iterativo(n)
        for funcao in (fib_memoizado, fib_iterativo):
            item = medir(funcao, n, args.repeticoes)
            escalabilidade.append(item)
            print(f"Escalabilidade: n={n:>3}  {item['algoritmo']:<17}  mediana={item['mediana_s']:.9f} s")

    # Não medir recursivo ingenuamente para n alto; seria inviável.
    for n in [500, 1000, 2000, 5000, 10000]:
        item = medir(fib_iterativo, n, args.repeticoes)
        escalabilidade.append(item)
        print(f"Escalabilidade: n={n:>5}, {fib_iterativo.__name__:<17}, {item['mediana_s']:.9f} s")
    salvar_csv(args.saida / 'av3_comparacao.csv', comparacao)
    salvar_csv(args.saida / 'av3_escalabilidade.csv', escalabilidade)
    registrar_ambiente(args.saida / 'ambiente.txt')
    print('Arquivos salvos em', args.saida.resolve())


if __name__ == '__main__':
    main()
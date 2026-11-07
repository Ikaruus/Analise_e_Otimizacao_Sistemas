"""Duas implementações de Fibonacci para a AV2 (original e memoizada).

Contrato comum: n deve ser int (exceto bool) e n >= 0.
Ambas retornam o valor exato F(n), com F(0)=0 e F(1)=1.
"""


def _validar(n: int) -> None:
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n deve ser um número inteiro")
    if n < 0:
        raise ValueError("n deve ser maior ou igual a zero")


def fib_original(n: int) -> int:
    """Versão original, recursiva, sem cache. Tempo O(2^n); espaço O(n)."""
    _validar(n)

    def calcular(k: int) -> int:
        if k < 2:
            return k
        return calcular(k - 1) + calcular(k - 2)

    return calcular(n)


def fib_memoizado(n: int) -> int:
    """Primeira otimização: memoização local. Tempo O(n); espaço O(n).

    O dicionário nasce vazio em CADA chamada pública, evitando que o
    benchmark da mesma entrada seja artificialmente favorecido por cache quente.
    """
    _validar(n)
    cache = {0: 0, 1: 1}

    def calcular(k: int) -> int:
        if k not in cache:
            cache[k] = calcular(k - 1) + calcular(k - 2)
        return cache[k]

    return calcular(n)

"""Medição reprodutível por lotes e medianas; não mede validação de correção."""
from __future__ import annotations
import csv
import datetime as dt
import platform
import statistics
import time
from pathlib import Path


def medir(funcao, n: int, repeticoes: int = 7, alvo_segundos: float = 0.03) -> dict:
    """Retorna tempo por execução com calibração de chamadas por amostra.

    Cada rodada executa a MESMA entrada n, sem reutilizar cache entre
    chamadas de fib_memoizado. A mediana reduz sensibilidade a outliers.
    """
    if repeticoes < 3:
        raise ValueError("Use no mínimo 3 repetições")
    inicio = time.perf_counter()
    funcao(n)
    estimativa = max(time.perf_counter() - inicio, 0.0000001)
    lote = max(1, min(10000, int(alvo_segundos / estimativa)))
    amostras = []
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        for _ in range(lote):
            funcao(n)
        decorrido = time.perf_counter() - inicio
        amostras.append(decorrido / lote)
    return {
        "n": n,
        "algoritmo": funcao.__name__,
        "mediana_s": statistics.median(amostras),
        "minimo_s": min(amostras),
        "media_s": statistics.mean(amostras),
        "lote": lote,
        "repeticoes": repeticoes,
    }


def salvar_csv(caminho: Path, linhas: list[dict]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(linhas[0]))
        writer.writeheader()
        writer.writerows(linhas)


def registrar_ambiente(caminho: Path) -> None:
    caminho.write_text(
        f"Data local da execução: {dt.datetime.now().isoformat(timespec='seconds')}\n"
        f"Sistema operacional: {platform.platform()}\n"
        f"Python: {platform.python_version()}\n"
        f"Processador (informado pelo sistema): {platform.processor() or 'não disponível'}\n"
        f"Medição: time.perf_counter(), mediana de 7 rodadas, lotes calibrados\n"
        f"Observação: execução em ambiente de referência, refazer na máquina do grupo.\n",
        encoding="utf-8", )

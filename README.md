## Comandos (PowerShell na pasta codigo)

```
python benchmarkAV2.py --saida ../resultados
python gerar_graficos.py --dados ../resultados --graficos ../graficos
```


Para gerar gráficos, instalar `matplotlib`: `python -m pip install matplotlib`.


## Arquivos Python incluídos

- `algoritmos.py`: versão original validada e primeira otimização memoizada.
- `medicao.py`: mede tempos de execução.
- `benchmark_av2.py`: compara os algoritmos e gera CSV.
- `gerar_graficos.py`: lê CSV e gera o gráfico da AV2.
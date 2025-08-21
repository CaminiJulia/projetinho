from __future__ import annotations
from typing import Iterable, List
import math
import statistics

def clean_numbers(data: Iterable[object], *, allow_negative: bool = True) -> List[float]:
    """
    Processa uma sequência com números possivelmente sujos (strings, None, espaços)
    e retorna uma lista de floats limpos.

    - Ignora None, vazios e NaN.
    - Converte strings "  10.5 " -> 10.5
    - Se allow_negative=False, remove números < 0.
    """
    cleaned: List[float] = []
    for item in data:
        if item is None:
            continue
        # normaliza strings
        if isinstance(item, str):
            s = item.strip()
            if not s:
                continue
            try:
                num = float(s.replace(",", "."))  # aceita "10,5"
            except ValueError:
                # se não dá pra converter, ignora
                continue
        elif isinstance(item, (int, float)):
            num = float(item)
        else:
            # tipos inesperados: ignora
            continue

        # descarta NaN / infinitos
        if math.isnan(num) or math.isinf(num):
            continue

        if not allow_negative and num < 0:
            continue

        cleaned.append(num)
    return cleaned


def summarize(numbers: Iterable[float]) -> dict:
    """
    Retorna um resumo estatístico: count, min, max, mean, median, stdev.

    - Lança ValueError se a lista estiver vazia após limpeza.
    - stdev é 0 quando houver 1 elemento (definimos assim explicitamente).
    """
    nums = list(numbers)
    if len(nums) == 0:
        raise ValueError("Lista de números vazia; impossível resumir.")
    return {
        "count": len(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": statistics.fmean(nums),
        "median": statistics.median(nums),
        "stdev": statistics.pstdev(nums) if len(nums) > 1 else 0.0,
    }

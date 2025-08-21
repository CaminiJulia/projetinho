import math
import pytest
from src.processor import clean_numbers, summarize
import sys
import os

# Adiciona o caminho do diretório 'src' ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))


# ---------- Testes para clean_numbers ----------

@pytest.mark.parametrize(
    "entrada,kwargs,esperado",
    [
        ([1, 2, 3], {}, [1.0, 2.0, 3.0]),
        ([" 10 ", " 20.5 ", "x"], {}, [10.0, 20.5]),
        (["10,5", None, "", "   "], {}, [10.5]),
        ([float("nan"), float("inf"), "-"], {}, []),
        ([-5, 0, 5], {"allow_negative": False}, [0.0, 5.0]),
        ([1, "2", 3.0], {}, [1.0, 2.0, 3.0]),
        (["not number"], {}, []),
    ],
)
def test_clean_numbers_casos_gerais(entrada, kwargs, esperado):
    assert clean_numbers(entrada, **kwargs) == pytest.approx(esperado)


def test_clean_numbers_tipos_inesperados_sao_ignorados():
    class X: ...
    assert clean_numbers([X(), {"a": 1}, [1, 2]]) == []

# ---------- Testes para summarize ----------

def test_summarize_lista_vazia_dispara_erro():
    with pytest.raises(ValueError):
        summarize([])

def test_summarize_um_elemento():
    out = summarize([10])
    assert out["count"] == 1
    assert out["min"] == 10
    assert out["max"] == 10
    assert out["mean"] == 10
    assert out["median"] == 10
    assert out["stdev"] == 0.0

def test_summarize_varios_elementos():
    out = summarize([1, 2, 3, 4])
    assert out["count"] == 4
    assert out["min"] == 1
    assert out["max"] == 4
    assert out["mean"] == pytest.approx(2.5)
    assert out["median"] == 2.5
    assert out["stdev"] == pytest.approx( math.sqrt(((1.5**2)+(0.5**2)+(0.5**2)+(1.5**2))/4) )

def test_fluxo_integrado_limpa_e_resume():
    sujos = [" 1 ", "2,5", None, "x", "-3", "  ", 10]
    limpos = clean_numbers(sujos, allow_negative=False)  # -> [1.0, 2.5, 10.0]
    out = summarize(limpos)
    assert out["count"] == 3
    assert out["min"] == 1.0
    assert out["max"] == 10.0

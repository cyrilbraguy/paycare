import pandas as pd
import pytest
from app.etl import transform_data, load_data  # adapte l'import


# ---------- Data Transformation ----------

@pytest.fixture
def raw_data():
    """Données brutes avec valeurs manquantes."""
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", None],
        "salary": [1000, 2000, None, 4000],
    })


def test_transform_data_drops_na(raw_data):
    """Les lignes contenant des NaN doivent être supprimées."""
    result = transform_data(raw_data)

    assert result is not None
    assert len(result) == 2  # seules Alice et Bob n'ont aucun NaN
    assert result.isna().sum().sum() == 0


def test_transform_data_tax_calculation(raw_data):
    """Vérifie le calcul de la taxe à 10%."""
    result = transform_data(raw_data)

    expected_tax = result["salary"] * 0.1
    pd.testing.assert_series_equal(result["tax"], expected_tax, check_names=False)


def test_transform_data_net_salary_calculation(raw_data):
    """Vérifie le calcul du salaire net = salaire - taxe."""
    result = transform_data(raw_data)

    expected_net = result["salary"] * 0.9
    pd.testing.assert_series_equal(result["net_salary"], expected_net, check_names=False)


def test_transform_data_specific_values():
    """Test avec des valeurs connues, pour éviter toute ambiguïté sur les calculs."""
    data = pd.DataFrame({"salary": [1000.0, 2000.0]})
    result = transform_data(data)

    assert result["tax"].tolist() == [100.0, 200.0]
    assert result["net_salary"].tolist() == [900.0, 1800.0]


def test_transform_data_missing_salary_column():
    """Colonne 'salary' absente -> KeyError attrapée, retourne None."""
    data = pd.DataFrame({"name": ["Alice", "Bob"]})
    result = transform_data(data)

    assert result is None


def test_transform_data_empty_dataframe():
    """DataFrame vide -> pas de crash, retourne un DataFrame vide (pas None)."""
    data = pd.DataFrame({"salary": []})
    result = transform_data(data)

    assert result is not None
    assert result.empty



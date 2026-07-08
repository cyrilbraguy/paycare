import pandas as pd
import pytest
from app.etl import transform_data, load_data  # adapte l'import

# ---------- Data Loading ----------

def test_load_data_creates_file(tmp_path):
    """Le fichier de sortie doit être créé avec le bon contenu."""
    data = pd.DataFrame({"salary": [1000, 2000], "net_salary": [900, 1800]})
    output_path = tmp_path / "output.csv"

    load_data(data, str(output_path))

    assert output_path.exists()
    result = pd.read_csv(output_path)
    pd.testing.assert_frame_equal(result, data)


def test_load_data_no_index_column(tmp_path):
    """Vérifie que l'index pandas n'est pas écrit dans le CSV (index=False)."""
    data = pd.DataFrame({"salary": [1000, 2000]})
    output_path = tmp_path / "output.csv"

    load_data(data, str(output_path))

    with open(output_path) as f:
        header = f.readline().strip()
    assert header == "salary"  # pas de colonne "Unnamed: 0" ou index


def test_load_data_invalid_path(capsys):
    """Chemin invalide (dossier inexistant) -> erreur attrapée, pas d'exception levée."""
    data = pd.DataFrame({"salary": [1000]})

    load_data(data, "/chemin/inexistant/output.csv")

    captured = capsys.readouterr()
    assert "Error in data loading" in captured.out


def test_load_data_overwrites_existing_file(tmp_path):
    """Un fichier existant doit être écrasé, pas fusionné/ajouté."""
    output_path = tmp_path / "output.csv"
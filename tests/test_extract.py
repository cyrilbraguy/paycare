import pandas as pd
import pytest
from app.etl import extract_data  # adapte l'import


@pytest.fixture
def valid_csv(tmp_path):
    """Crée un CSV valide temporaire."""
    file_path = tmp_path / "data.csv"
    pd.DataFrame({"id": [1, 2, 3],
    "name": ["John Doe", "Jane Smith", "Bob Johnson"],
    "age": [28, 34, 45],
    "city": ["New York", "Los Angeles", "Chicago"],
    "salary": [70000, 80000, 90000]}).to_csv(file_path, index=False)
    return file_path

# @pytest.fixture
# def mock_read_csv(mocker0):
#     """Mocke pd.read_csv pour retourner un DataFrame fixe, sans toucher au disque."""
#     fake_data = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
#     mocker = mocker0.patch("pandas.read_csv", return_value=fake_data)
#     return mocker


def test_extract_data_success(valid_csv, capsys):
    """Cas nominal : lecture réussie."""
    result = extract_data(str(valid_csv))

    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["id", "name","age","city","salary"]
    assert len(result) == 3

    captured = capsys.readouterr()
    assert "Data extraction successful." in captured.out

#@pytest.fixture
def test_extract_data_file_not_found(capsys):
    """Fichier inexistant -> retourne None, pas d'exception levée."""
    result = extract_data("chemin/inexistant.csv")

    assert result is None
    captured = capsys.readouterr()
    assert "Error in data extraction" in captured.out

#@pytest.fixture
def test_extract_data_empty_file(tmp_path, capsys):
    """CSV vide -> pandas lève EmptyDataError, capturée par le except."""
    file_path = tmp_path / "empty.csv"
    file_path.write_text("")

    result = extract_data(str(file_path))

    assert result is None
    captured = capsys.readouterr()
    assert "Error in data extraction" in captured.out

#@pytest.fixture
def test_extract_data_malformed_csv(tmp_path):
    """CSV avec nombre de colonnes incohérent selon les lignes."""
    file_path = tmp_path / "malformed.csv"
    file_path.write_text("col1,col2\n1,2,3\n4,5\n")

    result = extract_data(str(file_path))

    # pandas peut soit lever une erreur (-> None) soit gérer via tokenizing
    # selon la version ; on vérifie juste l'absence de crash
    assert result is None or isinstance(result, pd.DataFrame)

#@pytest.fixture
# def test_extract_data_uses_pd_read_csv(mocker, valid_csv):
#     """Vérifie que pd.read_csv est bien appelé avec le bon chemin."""
#     spy = mocker.spy(pd, "read_csv")
#     extract_data(str(valid_csv))
#     spy.assert_called_once_with(str(valid_csv))
    
    

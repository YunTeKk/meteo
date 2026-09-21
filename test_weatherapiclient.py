from unittest.mock import Mock, patch
import pytest
import requests
from weatherapiclient import WeatherAPIClient, CityNotFoundError, ApiNetworkError

client = WeatherAPIClient()

# test réponse API réussi
@patch("requests.get")
def test_get_coords_success(mock_get):

    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [{"latitude" : 48.8566, "longitude": 2.3522}]
    }
    mock_get.return_value = mock_response

    coords = client.get_coords("Paris")
    assert coords == (48.8566, 2.3522)

# test CityNotFoundError quand ville introuvable
@patch("requests.get")
def test_get_coords_city_not_found(mock_get):

    mock_response = Mock()
    mock_response.json.return_value = {"results" : []}
    mock_get.return_value = mock_response

    with pytest.raises(CityNotFoundError) as exc_info:
        client.get_coords("NoCityFound123")

    assert "Aucune ville trouvée" in str(exc_info.value)

# test timeout api géocode
@patch("requests.get")
def test_get_coords_network_timeout(mock_get):

    mock_get.side_effect = requests.exceptions.Timeout

    with pytest.raises(ApiNetworkError) as exc_info:
        client.get_coords("Paris")

    assert "[ERREUR] Aucune réponse du serveur de l'API de géocode." in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, requests.exceptions.Timeout)


# test erreurs HTTP api geocode
@patch("requests.get")
def test_get_coords_http_error(mock_get):

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")

    mock_get.return_value = mock_response

    with pytest.raises(ApiNetworkError):
        client.get_coords("Paris")

# test timeout api météo
@patch("requests.get")
def test_get_meteo_network_timeout(mock_get):

    mock_get.side_effect = requests.exceptions.Timeout

    with pytest.raises(ApiNetworkError) as exc_info:
        client.get_meteo(48.8566, 2.3522)

    assert "[ERREUR] Aucune réponse du serveur de l'API météo." in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, requests.exceptions.Timeout)


# test erreurs HTTP api météo
@patch("requests.get")
def test_get_meteo_http_error(mock_get):

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")

    mock_get.return_value = mock_response

    with pytest.raises(ApiNetworkError):
        client.get_meteo(48.8566, 2.3522)

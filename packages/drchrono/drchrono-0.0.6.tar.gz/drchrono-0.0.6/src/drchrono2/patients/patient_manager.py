from ..utils.httpclient import HttpClient
from .uris import ROOT_PATIENT_API

class PatientManager: 
    """

    A manager objects that provides a full interface to Drchrono Patient API.
    :param API_key: the drChrono API key
    :type API_key: str
    :returns: an `PatientManager` instance
    :raises: `AssertionError` when no API Key is provided
    
    """

    def __init__(self, API_key, config):
        assert isinstance(API_key, str), 'You must provide a valid API Key'
        self.API_key = API_key
        assert isinstance(config, dict)
        self.http_client = HttpClient(API_key, config, ROOT_PATIENT_API)

    def get_all(self):
        """
        Retrieves all of the patients based on permissions for logged in user.
        :returns: json 
        """

        status, data = self.http_client.get_json(
            path='/',
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.API_key})
            
        return {'status': status, 'data': data}



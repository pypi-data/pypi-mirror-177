import requests

class PATIENTS(object):

    def __init__(self, api_key, patient_id=None, fake_count=None, **kwargs):
        self.patient_id = patient_id
        self.fake_count = fake_count
        assert isinstance(api_key, str), 'You must provide a valid API Key'
        self.api_key = api_key

    @property
    def patientlist(self):
        path = 'https://drchrono.com/api/patients'
        list_response = []
        while path:
            data = requests.get(path, headers={'Authorization': 'Bearer ' + self.api_key})
            data_json = data.json()
            list_response.extend(data_json['results'])
            path = data_json['next']
        return list_response

    @classmethod
    def patient_single(cls, api_key, patient_id):
        path = 'https://drchrono.com/api/patients/{}'.format(patient_id)
        print('path: ', path)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + api_key})
            if data == 200:
                data_json = data.json()
                return data_json
            else:
                print('Error: {}'.format(data))
        except Exception as e:
            print(e)
import requests

class APPOINTMENTS(object):

    def __init__(self, api_key, appointment_startdate=None, appointment_enddate=None, appointment_id=None, fake_count=1, **kwargs):
        self.appointment_startdate = appointment_startdate
        self.appointment_enddate = appointment_enddate
        self.appointment_id = appointment_id
        self.fake_count = fake_count
        assert isinstance(api_key, str), 'You must provide a valid API Key'
        self.api_key = api_key

    @classmethod
    def appointment_list(cls, api_key, appointment_startdate=None, appointment_enddate=None):
        """
            Appointment startdate format: YYYY-MM-DD
            Appointment endate format: YYYY-MM-DD
        """
        path = 'https://drchrono.com/api/appointments?since={}'.format(appointment_startdate)
        list_response = []
        while path:
            data = requests.get(path, headers={'Authorization': 'Bearer ' + api_key}).json()
            list_response.extend(data['results'])
            path = data['next'] # A JSON null on the last page
        return list_response

    @classmethod
    def appointment_single(cls, api_key, appointment_id):
        path = 'https://drchrono.com/api/appointments/{}'.format(appointment_id)
        try: 
            data = requests.get(path, headers={'Authorization': 'Bearer ' + api_key})
            data_json = data.json()
            return data_json
        except Exception as e:
            print(e)
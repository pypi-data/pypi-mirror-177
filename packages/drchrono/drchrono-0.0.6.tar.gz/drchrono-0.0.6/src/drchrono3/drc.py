from . import constants
from .clinical import patient

"""
documentation section: https://app.drchrono.com/api-docs/#section/Introduction 
"""

class drc:

    """
    Entry point class providing ad-hoc API clients for each drChrono API.
    """

    def __init__(self, api_key):
        ## if api_key is None, display warning message
        assert api_key is not None, 'API Key must be set'
        self.api_key = api_key

    @property
    def version(self):
        """
        Returns the current version of the Drchrono API wrapper library
        :returns: `tuple`
        """
        return constants.DRC_VERSION

    @property
    def version_patients(self):
        """
        Returns the current version of the Drchrono API wrapper library
        :returns: `tuple`
        """
        return constants.PATIENTS_API_VERSION

    def patients(self):
        """
        Gives a `drc.patient_manager.patients` instance that can be used to read/write data from the
        patient API.
        """
        return patient.PATIENTS(self.api_key)





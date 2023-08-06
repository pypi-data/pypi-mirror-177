
from . import constants
from .patients import patient_manager
from .utils import config as cfg

class drc:

    """
    Entry point class providing ad-hoc API clients for each drChrono API.

    :param api_key: the OWM API key
    :type api_key: str
    :param version: the OWM API version

    """

    def __init__(self, api_key, config=None):
        assert api_key is not None, 'API Key must be set'
        self.api_key = api_key
        if config is None:
            self.config = cfg.get_default_config()
        else:
            assert isinstance(config, dict)
            self.config = config


    @property
    def version(self):
        """
        Returns the current version of the Drchrono API wrapper library
        :returns: `tuple`
        """
        return constants.DRC_VERSION

    def patient_manager(self):
        """
        Gives a `drc.patients.patient_manager` instance that can be used to read/write data from the
        patient API.
        :return: a `drc.patients.patient_manager` instance
        """
        return patient_manager.PatientManager(self.api_key, self.config)

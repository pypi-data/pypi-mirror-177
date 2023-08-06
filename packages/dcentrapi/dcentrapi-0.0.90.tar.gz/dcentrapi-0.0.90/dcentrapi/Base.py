import json
# from dcentrapi.common import get_dapi_version


class Base:

    def __init__(self, stage, username, key):

        self.__version__ = "0.0.88"
        
        if stage == 'develop':
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://test-api.dcentralab.com/"
        if stage == 'staging':
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://staging.dcentralab.com/"
        if stage == 'main':
            self.headers = {"Authorization": username + "," + key}
            self.url = "https://api.dcentralab.com/"

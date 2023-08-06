"""IPdon Python API"""

import requests
import orjson

class IPdon:
    """Queries the IPDon api (https://ipdon.com) to retrieve IP intelligence.       
       API supports token based authentication and returns all properties as part of the low-latency IP service.

       Usage example:
            token = "5ae79d31-6e48-4641-a0fd-bcee9cd30ff6" #Leave string "" empty to use the Free tier instead.
            ipdon = IPdon(token)
            response = ipdon.query("86.84.0.0")
            print(response)
    """

    __token = None          

    def __init__(self, token:str = "") -> None:
        self.__token = token

    def query(self, IPaddress:str, filterSectionOrField:str=""):
        """Queries the IPdon low-latency service and returns a dictionary with the response        
        The API can filter what needs to be returned by specifying this in filterSectionOrField"""

        url = "https://api.ipdon.com/{}".format(IPaddress)

        if filterSectionOrField != "":
            url += "/{}".format(filterSectionOrField)

        response = None
        obj = None

        try:
            response = requests.get(url, headers={'token': self.__token})
            response.raise_for_status()
        
        except requests.exceptions.HTTPError as err:            
            raise IPdon.IPdonException(err.response.text, err.response.status_code)
        
        try:
            obj = orjson.loads(response.text)
        except Exception:
            raise IPdon.IPdonException("JSON response could not be parsed", -1)

        return obj

    class IPdonException(Exception):
        """Exception raised by the IPdon service - or encountered when parsing the response"""
        code = None

        def __init__(self, text, code) -> None:            
            self.code=code
            try:
                resp = json.loads(text)
                text = resp['message']
            except:
                pass          
                        
            super().__init__(text + " ({})".format(code))

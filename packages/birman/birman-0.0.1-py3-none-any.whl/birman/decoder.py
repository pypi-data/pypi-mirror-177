"""
Birman
"""
from typing import Dict, List


class Decoder:
    """
    Decoder
    """
    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def _get_name(self, field: List[str]) -> str:
        name = field[0].split("name=")[1]
        name = name.strip()  # incase there is any formatting remaining
        return name.replace('"', "")

    def _get_value(self, field: List[str]) -> str:
        return field[2].strip()

    def decode(self) -> Dict:
        """
        :return: A Dict of multipart formdata fields e.g [name]: [name]: value
        :rtype Optional[Dict]:
        """
        fields = {}
        try:
            assert isinstance(self.data, bytes)
        except AssertionError:
            return {}
        _data_str = self.data.decode("utf-8")
        _data_str = _data_str.split("\r\nContent-Disposition")
        if len(_data_str) == 0:
            return {}
        data = _data_str[1:]
        for d in data:
            field = d.split("\n")
            name = self._get_name(field)
            value = self._get_value(field)
            fields[name] = {"name": name, "value": value}
        return fields

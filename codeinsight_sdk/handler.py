import abc
from typing import List


class Handler(abc.ABC):
    def __init__(self, client):
        self.client = client
        self.cls = None

    @abc.abstractmethod
    def get(self):
        pass

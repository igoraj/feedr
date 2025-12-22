from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseMonitor(ABC):
    @abstractmethod
    def check_for_updates(self) -> List[Dict[str, Any]]:
        """
        Checks for updates.
        Returns a list of dictionaries, where each dictionary represents an item:
        {
            "title": str,
            "link": str,
            "description": str,
            "date": str (or datetime),
            "id": str (unique identifier)
        }
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

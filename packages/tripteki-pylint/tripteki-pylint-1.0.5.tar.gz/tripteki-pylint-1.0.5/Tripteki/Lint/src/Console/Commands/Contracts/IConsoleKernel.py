from abc import ABC, abstractmethod
from typing import Union, Tuple, Optional, Any, cast

class IConsoleKernel (ABC):

    @abstractmethod
    def handle (self) -> None:
        """
        :rtype: None
        """
        pass
from typing import Union, Tuple, Optional, Any, cast
from shutil import copyfile
from os import getcwd
from os.path import dirname, realpath, abspath
from .Contracts.IConsoleKernel import IConsoleKernel

class LintCommand (IConsoleKernel):

    def handle (self) -> None:
        """
        :rtype: None
        """
        source = abspath (dirname (realpath (__file__))+"/../../../pylintrc")
        destination = abspath (getcwd ()+"/pylintrc")

        try:

            copyfile (source, destination)

        except IOError as thrower:

            # raise ValueError (thrower)
            raise Exception (thrower)
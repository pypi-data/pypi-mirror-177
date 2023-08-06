from .Commands.LintCommand import LintCommand

def initial () -> None:
    """
    :rtype: None
    """
    LintCommand ().handle ()
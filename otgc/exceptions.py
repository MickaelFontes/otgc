class OnBoardError(Exception):
    """Generic error related to the Onboard class."""


class OnBoardAuthentification(OnBoardError):
    """Login attempt on OnBoard failed."""


class OnBoardMenuError(OnBoardError):
    """Error linked to menu navigation on OnBoard."""

class Station:
    """Station model class."""
    def __init__(self, stationCode, stationName):
        self.stationCode = stationCode
        self.stationName = stationName


class Token:
    """ Token class"""
    def __init__(self, token):
        self.token = token



class StatusMessage:
    """ StatusMessage class.
        Stores the error messages and status in case of exception"""
    def __init__(self, status, message):
        self.status = status
        self.message = message



class Departure:
    """ Departure model class.
        Stores the information of trains departing from the station"""
    def __init__(self, plannedDateTime, direction, plannedTrack, trainCategory):
        self.plannedDateTime = plannedDateTime
        self.direction = direction
        self.plannedTrack = plannedTrack
        self.trainCategory = trainCategory

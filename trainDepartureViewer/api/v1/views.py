from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests
import logging
from trainDepartureViewer.api.v1.models import Departure, StatusMessage, Token, Station
from trainDepartureViewer.api.v1.serializers import TrainSerializer, StatusMessageSerializer, TokenSerializer, StationSerializer
from trainDepartureViewer.api.v1 import constants
from trainDepartureViewer.autz import credentials

logger = logging.getLogger(__name__)


@api_view(['GET'])
def get_stations(request):
    """ Gets all the stations by using get_stations_from_gateway method.
        request: request is a http request when the endpoint is hit."""
    logger.info('Entering get_stations method')

    response, is_valid_token = verify_token(request)
    if not is_valid_token:
        return response

    try:
        stations = get_stations_from_gateway()
    except requests.exceptions.Timeout:
        status_message = StatusMessage(
            status.HTTP_408_REQUEST_TIMEOUT, constants.CONNECTION_TIMEOUT)
        status_message_serializer = StatusMessageSerializer(status_message)
        logger.debug(constants.CONNECTION_TIMEOUT)
        logger.debug('Exiting get_stations method')
        return Response(status_message_serializer.data, status=status.HTTP_408_REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        status_message = StatusMessage(
            status.HTTP_502_BAD_GATEWAY, constants.BAD_GATEWAY)
        status_message_serializer = StatusMessageSerializer(status_message)
        logger.debug(constants.BAD_GATEWAY)
        logger.debug('Exiting get_stations method')
        return Response(status_message_serializer.data, status=status.HTTP_502_BAD_GATEWAY)
    except KeyError:
        status_message = StatusMessage(
            status.HTTP_500_INTERNAL_SERVER_ERROR, constants.KEY_ERROR)
        status_message_serializer = StatusMessageSerializer(status_message)
        logger.debug(constants.KEY_ERROR)
        logger.debug('Exiting get_stations method')
        return Response(status_message_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    station_serializer = StationSerializer(stations, many=True)
    logger.info('Exiting get_stations method')
    return Response(station_serializer.data)


@api_view(['GET', 'POST'])
def get_trains(request):
    """ Gets all the departures by using get_trains_from_gateway method.
        request: request is a http request when the endpoint is hit."""
    logger.info('Entering get_trains method')

    response, is_valid_token = verify_token(request)
    if not is_valid_token:
        return response

    if request.method == 'GET':
        stationCode = 'GVC'
    else:
        try:
            stationCode = request.data[constants.STATION_CODE]
        except:
            status_message = StatusMessage(
                status.HTTP_400_BAD_REQUEST, constants.STATION_CODE_MISSING)
            status_message_serializer = StatusMessageSerializer(status_message)
            logger.debug(constants.STATION_CODE_MISSING)
            return Response(status_message_serializer.data, status=status.HTTP_400_BAD_REQUEST)

    try:
        departure = get_trains_from_gateway(stationCode)
    except requests.exceptions.Timeout:
        status_message = StatusMessage(
            status.HTTP_408_REQUEST_TIMEOUT, constants.CONNECTION_TIMEOUT)
        status_message_serializer = StatusMessageSerializer(status_message)
        logger.debug(constants.CONNECTION_TIMEOUT)
        logger.debug('Exiting get_trains method')
        return Response(status_message_serializer.data, status=status.HTTP_408_REQUEST_TIMEOUT)
    except requests.exceptions.ConnectionError:
        status_message = StatusMessage(
            status.HTTP_502_BAD_GATEWAY, constants.BAD_GATEWAY)
        status_message_serializer = StatusMessageSerializer(status_message)
        logger.debug(constants.BAD_GATEWAY)
        logger.debug('Exiting get_trains method')
        return Response(status_message_serializer.data, status=status.HTTP_502_BAD_GATEWAY)
    except KeyError:
        status_message = StatusMessage(
            status.HTTP_500_INTERNAL_SERVER_ERROR, constants.KEY_ERROR)
        status_message_serializer = StatusMessageSerializer(status_message)
        logger.debug(constants.KEY_ERROR)
        logger.debug('Exiting get_trains method')
        return Response(status_message_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    departure_serializer = TrainSerializer(departure, many=True)
    logger.info('Exiting get_trains method')
    return Response(departure_serializer.data)


@api_view(['POST'])
def get_api_token(request):
    logger.info('Entering get_api_token method')

    try:
        username = request.data[constants.USERNAME]
        password = request.data[constants.PASSWORD]
        if username == credentials.USERNAME and password == credentials.PASSWORD:
            token = Token(credentials.TOKEN)
            token_serializer = TokenSerializer(token)
            logger.info('Exiting get_api_token method')
            return Response(token_serializer.data, status=status.HTTP_200_OK)
        else:
            status_message = StatusMessage(
                status.HTTP_401_UNAUTHORIZED, constants.UNAUTHORIZED_WARNING)
            status_message_serializer = StatusMessageSerializer(status_message)
            logger.debug(constants.UNAUTHORIZED_WARNING)
            logger.debug('Exiting get_api_token method')
            return Response(status_message_serializer.data, status=status.HTTP_401_UNAUTHORIZED)
    except Exception:
        status_message = StatusMessage(
            status.HTTP_400_BAD_REQUEST, constants.BAD_TOKEN_REQUEST)
        status_message_serializer = StatusMessageSerializer(status_message)
        logger.debug(constants.BAD_TOKEN_REQUEST)
        logger.debug('Exiting get_api_token method')
        return Response(status_message_serializer.data, status=status.HTTP_400_BAD_REQUEST)


def get_trains_from_gateway(station):
    """Returns the list of trains on a station """
    logger.info('Entering get_trains_from_gateway method')

    url = f'{constants.TRAIN_GATEWAY_URL}{constants.DEPARTURES}/{constants.STATION}{station}'
    headers = {credentials.KEY: credentials.VALUE}
    response = requests.get(url, headers=headers).json()
    departures = response[constants.PAYLOAD][constants.DEPARTURES]
    trains = []

    for departure in departures:
        plannedDateTime = departure[constants.PLANNED_DATE_TIME]
        direction = departure[constants.DIRECTION]
        plannedTrack = departure[constants.PLANNED_TRACK]
        trainCategory = departure[constants.TRAIN_CATEGORY]
        trainCategory = get_train_category(trainCategory)
        trains.append(Departure(plannedDateTime, direction,
                      plannedTrack, trainCategory))

    logger.info('Exiting get_trains_from_gateway method')
    return trains


def get_stations_from_gateway():
    """Returns the list of trains on station a station """
    logger.info('Entering get_stations_from_gateway method')
    
    url = f'{constants.TRAIN_GATEWAY_URL}{constants.STATIONS}'
    headers = {credentials.KEY: credentials.VALUE}
    response = requests.get(url, headers=headers).json()
    stationList = response[constants.PAYLOAD]
    stations = []
    for station in stationList:
        stationCode = station[constants.CODE]
        stationName = station[constants.NAMEN][constants.LANG]
        stations.append(Station(stationCode, stationName))

    logger.info('Exiting get_trains_from_gateway method')
    return stations


def get_train_category(train_acronym):
    """ Returns the train category from acronym 
        train_acronym: str acronym for train category. """
    logger.info('Entering get_train_category method')

    logger.info('Exiting get_train_category method')
    if train_acronym == constants.IC:
        return constants.INTER_CITY
    elif train_acronym == constants.SPR:
        return constants.SPRINTER
    else:
        return train_acronym


def verify_token(request):
    logger.info('Entering verify_token method')

    try:
        if request.headers['Authorization'] == (f'{constants.TOKEN}{credentials.TOKEN}'):
            logger.info('Exiting verify_token method')
            return None, True
    except:
        status_message = StatusMessage(
        status.HTTP_401_UNAUTHORIZED, constants.TOKEN_NOT_FOUND)
        status_message_serializer = StatusMessageSerializer(status_message)
        logger.debug(constants.TOKEN_NOT_FOUND)
        logger.debug('Exiting verify_token method')
        return Response(status_message_serializer.data, status=status.HTTP_401_UNAUTHORIZED), False

    status_message = StatusMessage(
    status.HTTP_401_UNAUTHORIZED, constants.TOKEN_NOT_FOUND)
    status_message_serializer = StatusMessageSerializer(status_message)
    logger.debug(constants.TOKEN_NOT_FOUND)
    logger.debug('Exiting verify_token method')
    return Response(status_message_serializer.data, status=status.HTTP_401_UNAUTHORIZED), False

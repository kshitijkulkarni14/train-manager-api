# Train Viewer

A django api project to get the information about all the train stations in netherlands and the train departing from the station.

## Installation

In order to run the django api the below steps can be followed.

1.Run the below command to install all the required libraries

```bash
pip install -r requirements.txt
```

2.Run the below command to make the api available to use

```bash
python manage.py runserver
```


## Usage

### API Reference

#### Get api token

```http
  POST /api/v1/api-token/
```

| Parameter  | Type     | Description                 |
| :--------- | :------- | :-------------------------- |
| `username` | `string` | **Required**. Your username |
| `password` | `string` | **Required**. Your password |

#### Get all stations

```http
  GET /api/v1/stations/
```

| Header          | Type     | Description                 |
| :-------------- | :------- | :-------------------------  |
| `Authorization` | `string` | **Required**. Your API token|


#### Get all departures from a station

```http
  POST /api/v1/trains/
```

| Parameter       | Type     | Description                |
| :-------------- | :------- | :------------------------- |
| `stationCode`   | `string` | **Required**. The station code you want to explore |

| Header          | Type     | Description                 |
| :-------------- | :------- | :-------------------------  |
| `Authorization` | `string` | **Required**. Your API token|
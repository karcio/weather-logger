# weather-logger

## Software

- python3
- python3-pip
- python3-venv
- mosquitto
- mosquitto-clients

## manual start application

1. install python3

2. create virt env

```
python3 -m venv virtenv
```

3. source virt env

```
source virtenv/bin/activate
```

4. install dependencies

```
pip install --upgrade pip
pip install -r requirements.txt
```

5. run script

```
python src/getWeather.py
```

## Docker

1. build image

```
docker image build -t karcio/weather-logger .

```

2. run docker container

```
docker run -d --name=weather-logger --restart unless-stopped karcio/weather-logger
```

3. see logs

```
docker logs -f weather-logger
```

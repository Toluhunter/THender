# THender (Tolu Hunter's sender)

## Overview
A file transfer websocket application, built using django rest framework application to enable cross platform transfer of data i.e (music, videos, executables, documents) without being stored on an intermediary server. This ensures data privacy and provides an alternative method of sending large files accross the internet without dealing with the complexities of torrents or the limitations of cloud storage

## Usage

This system is designed to be run on a remote server this allows the forwarding of data between users without storage

### Instructions

1. Setup required enironment variables, you can do this by adding it to the the system global environmnet variables or by creating a **.env** and placing it in the config directory, as of now the only required environment variable is **SECRET_KEY** Note: it is case sensitive

2. Install depenencies in the requirements.txt using this command `pip install -r requirements.txt`, then use the command `python manage.py runserver 0.0.0.0:<port>` to run the server. Alternatively you can make use of docker which is recommended, have docker installed on your system then run the following commands:

```
docker build -t thender .
docker run -dp 8000:8000 thender
```

3. Now port 8000 would be open on your system/server. view the [Postman Doc link](https://documenter.getpostman.com/view/24863856/2s93CRMCMc) for instructions on how to use api

## How to Contribute 


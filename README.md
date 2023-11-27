### Table of contents
- [General info](#general-info)
  * [Description](#description)
  * [Screenshots](#screenshots)
- [Installation](#installation)
- [Configuration](#configuration)


# General info

## Description

Animal scanner backend is a RESTful API powering Animal Scanner frontend. It integrates Nominatim API for geosearch and uses PostgreSQL database server.

## Screenshots

-  Auth router
![obraz](https://github.com/kAleks12/animal-scanner-backend/assets/79469983/697fe7e0-771a-40ef-bbe6-ad1b602ec2f3)

-  Submission router
![obraz](https://github.com/kAleks12/animal-scanner-backend/assets/79469983/3a1306ca-e57a-4fdf-9167-dc22d8fdf3f4)

-  Search router
![obraz](https://github.com/kAleks12/animal-scanner-backend/assets/79469983/68c015c4-10c5-4bcd-93dc-a4c5b8ee7667)



# Installation
1. Install docker on your system
2. Clone this repo and open its directory in file explorer
3. Open terminal in said directory
4. Enter these commands
```
cd docker
docker compose up -d
```
5. Swagger UI should be accessible by default under
```
http://localhost:8080/docs
```

# Configuration
Config file is named `config.ini` and it contains all the changeable settings for the API. Defined parameters are:
* **server** section
  - **host** - host address of the API, default is 127.0.0.1
  - **port** - port of the API, default is 8081
  - **prefix** - prefix of the API, default is "/api/v1"
  - **allow_origins** - list of allowed origins, default is * (all)
  - **allow_methods** - list of allowed origins, default is * (all)
  - **allow_headers** - list of allowed origins, default is * (all)
  - **docs** - enable/disable swagger docs available under `host\port\docs`, default is 1 (on)
  - **redoc** - enable/disable redoc docs available `host\port\redoc`, default is 1 (on)
* **database** section
  - **host**
  - **port**
  - **user**
  - **password**
  - **db_name**
  - **connect_attempts** - number of connection attempts
* **auth** section
  - **<key>_token_secret** - base key for generating <key> token
  - **<key>_token_exp_min** - length of <key> token time to live
* **email** section
  - **smtp_server** - smtp server provider
  - **smtp_port**
  - **user**
  - **password**
  - **sender_name**
* **config** section
  - **upload_dir** - directory for uploaded photos

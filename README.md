# Reddit stock data scraper
Web application which scraps most mentioned stocks 
from selected subredits. With the use of yahoo finance website
retrieves information about given stock. Results are presented
on simple react frontend, charts are displayed by using recharts.
User can also find stocks by giving its ticker.
Scrapping is scheduled to scrap reddit and update stock information 
via yahoo finance.
## Installation
Before running .env files should be configured
1. Flask `app/.env`
```bash
REDDIT_CLIENT_ID={REDDIT_CLIENT_ID}
REDDIT_SECRET={REDDIT_SECRET}
REDDIT_USER_AGENT=StockDataScraper:1.0.0 (by dawid glinkowski)
MONGODB_USERNAME=
MONGODB_PASSWORD=
MONGODB_HOSTNAME=mongodb 
MONGODB_DATABASE=flaskdb
```
Get reddit api keys on [Reddit apps](https://www.reddit.com/prefs/apps)

2. React  `reddit-scraper-frontend/.env`
    
```bash
    REACT_APP_STOCK_API_URL = 'http://localhost:5000/api/v1/stocks/'
```

### Running on docker
Before running application, build all docker images
```bash
$ docker compose build
```

#### Mongo configuration
Run mongodb image and through its terminal login to database
```bash
$ mongosh -u {username from docker compose}
```
After login change database to flaskdb and add user with credentials
same as in `/app/.env` file
```
    use flaskdb
    db.createUser({
        user: "MONGODB_USERNAME",
        pwd:  "MONGODB_PASSWORD",   
        roles: [ { role: "readWrite", db: "flaskdb" } ]
    })
```
To start docker app run
```
$ docker compose up
```

### Running without docker
#### Mongo 
In order to run outside the docker, change in `app/.env`  *MONGODB_HOSTNAME* 
to address of mongo server, on local machine it is localhost. 
#### Flask
To run flask application install all dependencies from `app/requirements.txt`
```bash
$ pip install -r requirements.txt
```
Run flask backend server
```bash
$ python3 -m flask run
```
#### React
Install dependencies from `package.json`
```bash
 $ npm i
```
Start react server at localhost:3000 
```bash
 $ npm start
```
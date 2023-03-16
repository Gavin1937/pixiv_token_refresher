
# pixiv_token_refresher

A simple python utility to refresh your pixiv token

## requirement

* python >= 3.8
* requests >= 2.28.1
* sqlalchemy >= 2.0.6 (optional, for db operations)

### install all requirements with following command

```sh
pip install -r requirements.txt
```

or, if you want to [store your token in database](#database)

```sh
pip install -r requirements_db.txt
```

## configuration

You need to create a **token.json** file before running the program

sample **token.json** file

```jsonc
{
  "access_token": "your access token",
  "refresh_token": "your refresh token",
  "expires_in": 3600
}
```

* you can use [token_template.json](./token_template.json) as your foundation

* Note that new tokens will be **print to stdout** and **write to token.json**

## usage

After you setup your **token.json**, simply run **refresher.py** file

```sh
python refresher.py
```

Or, you can import refresher form **refresher.py** and use its api

```py
from refresher import refresher

try:
    ref = refresher()
    token = ref.do_refresh()
    # print(token)
except Exception as err:
    print(err)
    exit(-1)
```

## automation

You can easily automate the whole process with system build-in features like crontab (Unix), systemd(Unix), and Windows Services Manager (Windows)

## database

If you want to store your token into a database

You can use [updatedb.py](./updatedb.py) instead.

Create another configuration file: **config.json**

```jsonc
{
  "connect_str": "your connection string"
}
```

You can use [config_template.json](./config_template.json) as your foundation

And then, simply run [updatedb.py](./updatedb.py) file

```sh
python updatedb.py
```

This program uses sqlalchemy to handle database operations, follow [their guide](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls) for connection string

* Note that you may need to install additional packages for sqlalchemy to work with your database
  * e.g. you need to install `pymysql` if you wanna use `mysql+pymysql` in your connection string

* Table in database

```sql
CREATE TABLE pixiv_token (
  id              INTEGER PRIMARY KEY AUTOINCREMENT   NOT NULL,
  access_token    VARCHAR(50)                         NOT NULL,
  refresh_token   VARCHAR(50)                         NOT NULL,
  expires_in      INTEGER                             NOT NULL, -- expiration time in seconds
  refresh_at      INTEGER                             NOT NULL  -- unix timestamp, last refresh time
);
```

## credits

* [pixiv_auth.py from upbit](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde)
* [sqlalchemy](https://www.sqlalchemy.org/)

## if you want to login

follow the [upbit's guide](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde)

you can use **pixiv_auth.py** in the repo, they are the same

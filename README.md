
# pixiv_token_refresher

A simple python utility to refresh your pixiv token

## requirement

* python >= 3.8
* requests >= 2.28.1

### install all requirements with following command

```sh
pip install -r requirements.txt
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

## credits

* [pixiv_auth.py from upbit](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde)

## if you want to login

follow the [upbit's guide](https://gist.github.com/upbit/6edda27cb1644e94183291109b8a5fde)

you can use **pixiv_auth.py** in the repo, they are the same

# marvelapi
Script that asynchronously calls Marvel's API

## Setup

* Create a virtual env. [Click here to learn more about venv](https://docs.python.org/3/library/venv.html).

* Register for a Marvel account and generate your API keys [here](https://developer.marvel.com). 

* Initialize the following environment variables in your virtual env:
  * PUBLIC_KEY
  * PRIVATE_KEY
  
* Install the dependencies

  * This script uses `requests`, `aiofiles`, and `aiohttp`.

  * ```pip install -r requirements.txt```

## Usage

The script currently pulls *all* data that is available. This may take a significant amount of time.

You can modify this line if you don't want to pull *all* data:

  * ```tasks = [cache_data(obj) for obj in MARVEL_OBJ]```

  * If you only wanted to pull `characters` and `creators`, change that line to:
    * ```tasks = [cache_data('characters'), cache_data('creators')]```



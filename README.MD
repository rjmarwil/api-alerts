# API Alerts
A Python module to generate an alert if a currency pair's current price
is more than one standard deviation from its 24hr average.


## Setup
* [Required] Clone the [api-alerts](https://github.com/rjmarwil/api-alerts) git repository
* [Required] Ensure Python 3 is installed
    * `python` command should be symlinked to your Python 3 installation, otherwise use `python3`
    * You can also install/use [virtualenv](https://virtualenv.pypa.io/en/latest/) if you prefer
* [Optional] Install Docker if you want to run the Docker container
    * [Docker Personal](https://www.docker.com/products/personal) is a good place to start
* [Optional] Install [jq](https://stedolan.github.io/jq/) if you would like the JSON output to be pretty printed
    * Once installed, you can pipe commands in the Run section below to jq, like so:
    * ```shell
      $ python3 api_alerts.py | jq .
      ```

## Run
After cloning the repo, this script can be run locally or with Docker.

*Note: This script was written and tested using Python 3.9.6. Check Setup section above to determine which version your `python` command is running.*

### Locally
#### Run with the `-h` option to view usage, descriptions, and arguments:

```shell
$ python3 api_alerts.py -h

usage: api_alerts.py [-h] [-c CURRENCY] [-d DEVIATION] [-s]

Runs checks on API

optional arguments:
  -h, --help            show this help message and exit
  -c CURRENCY, --currency CURRENCY
                        The currency trading pair, or ALL
  -d DEVIATION, --deviation DEVIATION
                        percentage threshold for deviation
  -s, --symbols         list available trading pairs
```

#### Run with default values (i.e. currency=btcusd, deviation=1):
(If you do not have `jq` installed, remove `| jq .` from below command)

```shell
$ python3 api_alerts.py | jq .
```

Expected output will be in the following format:
```json
{
  "timestamp": "2022-01-18T06:43:04.758514+00:00",
  "level": "INFO",
  "trading_pair": "ethusd",
  "deviation": true,
  "data": {
    "last_price": "3196.82",
    "average": "3230.38",
    "change": "33.56",
    "sdev": "1.04"
  }
}
```

#### Run by specifying a currency and deviation:

```shell
$ python3 api_alerts.py -c ethusd -d 1.2
```

#### Run with the `-s` or `--symbols` flag to see available currency pairs:

```shell
$ python3 api_alerts.py -s
```

### Docker
*Note: Please ensure docker is installed and started before running these commands. Check the Setup section above for recommendations.*

Build the docker image (run from within the app directory):
```shell
$ docker build -t api_alerts .
```

Run the docker image (If you do not have `jq` installed, remove `| jq .` from below command): 
```shell
$ docker run --rm api_alerts | jq .
```
This will start the docker container, run the python script, output the information to standard out, then delete the container once it's finished running.


## Dependencies
* Written and tested using Python 3.9.6.
* Linted using pylint 2.12.2.
* Used Requests module 2.27.1.


## Further Improvements
This script could be further improved by:
* Adding true logging for ERROR and DEBUG levels (only INFO is hard coded).
* Including a check on the currency flag making sure it's an available symbol.


## Other interesting checks to alert on market behaviour
* Set up ability to alert when a currency pair goes above or below a specified price.
* Set an alert to fire when a new symbol to trade becomes available at Gemini.
* Create alerting that tracks trading activity tied to specific wallet addresses.
* Alert when ETH gas prices reach a specified threshold.


## Approach to solving the task, and issues faced with implementation

### Approach
1. I read through the prompt a few times to get a sense of what would be needed.
2. I visited the API docs to figure out which endpoints would help me solve the problem. The four endpoints below seemed to have the most relevant data. Ticker V2 turned out to be the key endpoint to solve the issue.
    * [Symbols](https://docs.gemini.com/rest-api/#symbols)
    * [Ticker](https://docs.gemini.com/rest-api/#ticker)
    * [Ticker V2](https://docs.gemini.com/rest-api/#ticker-v2)
    * [Price Feed](https://docs.gemini.com/rest-api/#price-feed)
3. I started my code with argparser to implement the alert inputs as CLI args. Doing this helps me outline what the script should accomplish.
4. I then started by creating the methods to retrieve data from API endpoints and started to manipulate the data.
5. I then fleshed out the logic in my main method, checking calculations, and formatting the output.
6. Once I had the script running, I ran pylint to fix up any issues and make sure the code was passing 10/10.
7. I made a simple Dockerfile to spin up a python container to run the script.
8. I read through the prompt more times to ensure I had included everything that was asked.

### Issues Faced
* Got caught up trying to turn the output from the TickerV2 API endpoint request into an easily accessible dict.
* I ended up confusing the syntax to grab the info; was attempting `price_info.close` vs `price_info['close']`.
* Figured out my calculations weren't working at first because all values returned were strings. Had to spend time coercing to floats, etc..., as well as ensuring values were formatted properly (such as prices showing two decimal points).
* My docker container wasn't initially outputting anything to stdout, even though the container was properly running. Found that including the `PYTHONUNBUFFERED=1` ENV in the Dockerfile flushes output to stdout immediately, allowing python print statements to be seen in stdout.

### Other Considerations
I decided to include the method to get symbols because I noticed the error output for an incorrect currency wasn't very pretty or helpful. In case a user needed to run the script and wasn't sure of available symbols, I thought it made sense to alert them about finding them with the `-s` flag.


## Time it took to write this
I used the full 4 hour time period. 

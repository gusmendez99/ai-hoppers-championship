# AI - Hoppers Tournament
[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

The client was tested with [@RobertoFigueroa](https://github.com/RobertoFigueroa)'s Minimax, and whole code was not included for the obvious reason of being a tournament


## Demo
![demo](https://github.com/gusmendez99/ai-hoppers-tournament/raw/main/images/hoppers.gif?raw=true)

## Install
You need to create a virtual env and install libs from `requirements.txt`

Then, you need to clone Hoppers Lib into root folder
```shell
git clone https://github.com/RobertoFigueroa/hoppers-minimax-lib hoppers
```

Ready, we will have a `hoppers` folder to play

## Usage
Please make sure to complete all `TODOs` declared within `client.py`
### Server
```shell
./python server.py <port>
```  

### Client
```shell
./python client.py <server-ip> <server-port>
```

We have added a `test_client.py` that includes a Dummy Minimax AI Agent. If you want to use it, you must code your own `min_value`,  `max_value` and
`eval_function` (heuristic).
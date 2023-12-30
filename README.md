# coin-sentiment

Colelct posts from subreddit about crypto and apply sentiment analysis

## Prerequisites

### Setup venv 

```bash
python3 -m virtualenv ~/.venv # or make venv
source ~/.venv/bin/activate
```

Clean to to remove previous venv and python binaries.

```bash
rm -rf venv
```

### Credentials

To create credentials use `./scripts/create_credentials.sh` or `make credentials`

```json
{
    "reddit": {
        "USER_KEY": "",
        "SECRET_KEY": "",
        "PSW": "",
        "USERNAME": ""
    }
}
```

Fill the empty fields

### Installation

To install the required dependencies, run the following commands:

```bash
make install
```

Equal to 

```bash
pip install --upgrade pip &&\
    pip install -r requirements.txt
```

# Run App Flask

To run the App Flask 

```bash
make run
```


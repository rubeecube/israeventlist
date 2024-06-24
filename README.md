# Setup
1. Go to the botfather and create a bot : https://t.me/BotFather
2. Get the user and token
3. Copy the file `Storage/config.sample.py` to `Storage/config.py`
4. Insert your Token:

```
TOKEN = {
    "BotName_bot": "ID:TOKEN"
} 
```

# Run with Docker
`docker build -t maasser-image . && docker run -it maasser-image`

# Run without Docker
`python3 app/maasser_main.py`
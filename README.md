# passbolt_api_hibp_test
A simple script that checks your passbolt stored passwords against HIBP via APIs.

First install the dependencies
```
pip3 install -r requirements.txt
```
Edit config.ini and then run:
```
python3 passbolt_api_hibp_test.py
```

Caveat: The script in question utilizes a compression and encryption mechanism to safeguard the integrity of the password set contained within a pickle file, this is to avoid overwhelming of the HIBP servers.


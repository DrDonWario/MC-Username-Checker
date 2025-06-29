# MC-Username-Checker
Simple Python script to check the availability of Minecraft usernames using the Mojang API. This tool supports multiple checking methods and proxy functionality for rate limit handling.

## Features

- Multiple username checking methods:
- Check all available 3-character username combinations. 
- Check usernames from a custom word lists "words.txt" (Optional) any customized lists e.g. "localized.txt" is used to check specific language dictionnary word. Can be anything tho, just replace the .py with your custom name .txt filename or just put anything
  in the localized.txt. (It's just for personal organization purposes so, optional)
- Single manual input username checking
- Proxy support with automatic failover
- Rate limit handling with multiple options to choose from (wait, change proxy...)
- Logs for tracking results or fail. 
- Automatically saves available usernames to a file

## Requirements

- Python 3.x 
- pip
- At least an IQ of 80 (IMPORTANT)
## Installation

1. Download the py script from this git releases page
2. (if needed) Get the the "requests" packages:

$ pip install requests 
or 
$ python -m pip install requests
## Configuration
### Proxy Setup (More than one proxy recommended if multiple accounts)

Create a proxies.txt file in the same directory of the python script with your proxies in the following format:

- "user:password:host:port"
## Usage
Run the script:
cd in the script dir and type:
$ py script.py
### Menu Options

1. 3-Character Combinations
     - Generates and checks all possible 3-character combinations
     - Uses alphanumeric characters (a-z, A-Z, 0-9)

2. Word List Check
     - Choose between two word lists:
       - words.txt
       - e.g. localized.txt
     - Only checks words between 3-5 characters

3. Single Username Manual Check   
     - Manual username check
### Output Files

- available_usernames.txt : List of available usernames found
- logs.txt : Detailed log of all operations
## Rate Limiting
When rate limit is reached (HTTP 429), you have three options:

1. Wait 600 seconds timeout to reset mojang api rate limit and continue the search
2. Switch to a different proxy (if proxies.txt contains only one or used all proxies provided)
3. Return to main menu
## Notes
- The script automatically handles proxy rotation when rate limits are encountered
- All results are logged for future reference
- Available usernames are automatically saved in a file
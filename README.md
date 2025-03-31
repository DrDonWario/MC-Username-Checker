# MC-Username-Checker

A Python tool to check the availability of Minecraft usernames using the Mojang API. This tool supports multiple checking methods and proxy functionality for rate limit handling.

## Features

- Multiple username checking methods:
  - Generate and check all 3-character combinations
  - Check usernames from word lists (words.txt or francais.txt)
  - Manual username checking
- Proxy support with automatic failover
- Rate limit handling with multiple options
- Logging system for tracking results
- Saves available usernames to a file

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone the repository
2. Install the required dependencies:
```bash
pip install requests


## Configuration
### Proxy Setup (Optional)
Create a proxies.txt file in the same directory with your proxies in the following format:

```plaintext
user:password:host:port
 ```

## Usage
Run the script:

```bash
python script.py
 ```

### Menu Options
1. 3-Character Combinations
   
   - Generates and checks all possible 3-character combinations
   - Uses alphanumeric characters (a-z, A-Z, 0-9)
2. Word List Check
   
   - Choose between two word lists:
     - words.txt
     - francais.txt
   - Only checks words between 3-5 characters
3. Manual Check
   
   - Enter usernames manually to check availability
### Output Files
- available_usernames.txt : List of available usernames found
- logs.txt : Detailed log of all operations
## Rate Limiting
When rate limit is reached (HTTP 429), you have three options:

1. Wait 600 seconds and continue
2. Switch to a different proxy
3. Return to main menu
## Notes
- The script automatically handles proxy rotation when rate limits are encountered
- All results are logged for future reference
- Available usernames are automatically saved

from bitcoin_checker import is_valid_address

# use the is_valid_address function in your code

import bitcoin

# Wallet address to be checked
address = '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2'

# Validate the wallet address
valid = bitcoin.validate_address(address)

if valid:
    print('The wallet address is valid.')
else:
    print('The wallet address is invalid.')

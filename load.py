import json
import os

# Function to load wallet addresses from wallets.json
def load_wallet_addresses():
    try:
        # Print the current working directory (for debugging)
        print(f"Current working directory: {os.getcwd()}")
        
        # Open wallets.json to load the data
        with open('wallets.json', 'r') as f:
            data = json.load(f)
            # Extract only the addresses
            wallet_addresses = [wallet['address'] for wallet in data['wallets']]
        return wallet_addresses
    except Exception as e:
        print(f"Gagal memuat wallets.json: {str(e)}")
        return []

# Function to save the addresses to wallet.txt
def save_addresses_to_file(addresses):
    try:
        with open('wallet.txt', 'w') as f:
            # Write each address to a new line in wallet.txt
            for address in addresses:
                f.write(f"{address}\n")
        print("Alamat berhasil disalin ke wallet.txt")
    except Exception as e:
        print(f"Gagal menyimpan alamat ke wallet.txt: {str(e)}")

# Main function to load and save addresses
def copy_addresses():
    # Load wallet addresses from wallets.json
    wallet_addresses = load_wallet_addresses()

    # If addresses are found, save them to wallet.txt
    if wallet_addresses:
        save_addresses_to_file(wallet_addresses)
    else:
        print("Tidak ada alamat ditemukan di wallets.json.")

# Run the function to copy addresses
copy_addresses()


import os
import json
import random
from web3 import Web3
import time
from datetime import datetime, timedelta
from colorama import Fore, Style, init
from eth_account import Account  # Untuk menghasilkan wallet EVM baru

# Inisialisasi Colorama
init(autoreset=True)

CHECK_MARK = Fore.GREEN + "✔️" + Style.RESET_ALL
CROSS_MARK = Fore.RED + "❌" + Style.RESET_ALL
BALANCE_SYMBOL = Fore.CYAN + "💰" + Style.RESET_ALL
ETH_SYMBOL = Fore.YELLOW + "Ξ" + Style.RESET_ALL
SENDER_ADDRESS_SYMBOL = Fore.CYAN + "📤 Alamat Pengirim:" + Style.RESET_ALL
RECEIVER_ADDRESS_SYMBOL = Fore.MAGENTA + "📥 Alamat Penerima:" + Style.RESET_ALL
AMOUNT_SYMBOL = Fore.LIGHTYELLOW_EX + "💵 Jumlah Kiriman:" + Style.RESET_ALL

# Koneksi ke Ethereum Sepolia
web3 = Web3(Web3.HTTPProvider('https://autumn-cosmological-scion.unichain-sepolia.quiknode.pro/c568806873f2a9edb9fcdea8aef0569ff729eb25'))

if web3.is_connected():
    print(Fore.GREEN + f"Terkoneksi dengan jaringan Ethereum {CHECK_MARK}")
else:
    print(Fore.RED + f"Gagal terhubung ke jaringan Ethereum {CROSS_MARK}")
    raise Exception("Gagal terhubung ke jaringan Ethereum")

# Membaca multiple wallet dari file wallets.json
def load_wallets():
    if not os.path.exists('wallets.json'):
        print(Fore.YELLOW + "wallets.json tidak ditemukan, membuat file baru...")
        return []  # Jika belum ada file, kembalikan list kosong
    try:
        with open('wallets.json', 'r') as f:
            data = json.load(f)
        return data.get('wallets', [])
    except Exception as e:
        print(Fore.RED + f"Gagal membaca file wallets.json: {str(e)}")
        return []

# Menambahkan wallet baru ke wallets.json
def add_wallet():
    print(Fore.YELLOW + "=" * 50)
    print(Fore.CYAN + "1. Import Wallet")
    print(Fore.MAGENTA + "2. Generate New Wallet")
    print(Fore.YELLOW + "=" * 50)
    choice = input("Pilih opsi (1/2): ")

    if choice == "1":
        import_wallet()
    elif choice == "2":
        generate_new_wallet()
    else:
        print(Fore.RED + "Pilihan tidak valid. Silakan pilih 1 atau 2.")
        add_wallet()

# Mengimpor wallet yang sudah ada
def import_wallet():
    sender_address = input("Masukkan Alamat Wallet: ")
    private_key = input("Masukkan Private Key Wallet: ")
    
    # Membaca wallet yang ada
    wallets = load_wallets()

    # Menambahkan wallet baru
    new_wallet = {"address": sender_address, "private_key": private_key}
    wallets.append(new_wallet)

    # Menyimpan wallet ke file wallets.json
    try:
        with open('wallets.json', 'w') as f:
            json.dump({"wallets": wallets}, f, indent=4)
        
        print(Fore.GREEN + f"Wallet baru berhasil ditambahkan: {sender_address}")
    except Exception as e:
        print(Fore.RED + f"Gagal menyimpan wallet ke wallets.json: {str(e)}")

# Membuat wallet baru (EVM)
def generate_new_wallet():
    num_wallets = int(input("Berapa wallet yang ingin Anda buat? (Maksimal 50): "))
    if num_wallets < 1 or num_wallets > 50:
        print(Fore.RED + "Jumlah wallet harus antara 1 dan 50.")
        generate_new_wallet()
        return
    
    wallets = load_wallets()  # Membaca wallet yang ada

    for _ in range(num_wallets):
        account = Account.create()  # Membuat akun baru
        new_wallet = {"address": account.address, "private_key": account.key.hex()}  # Menggunakan 'key' bukan 'privateKey'
        wallets.append(new_wallet)

    # Menyimpan wallet baru ke file wallets.json
    try:
        with open('wallets.json', 'w') as f:
            json.dump({"wallets": wallets}, f, indent=4)
        
        print(Fore.GREEN + f"{num_wallets} wallet baru berhasil dibuat dan ditambahkan.")
    except Exception as e:
        print(Fore.RED + f"Gagal menyimpan wallet ke wallets.json: {str(e)}")

# Mengambil saldo
def get_balance(address):
    balance = web3.eth.get_balance(address)
    return web3.from_wei(balance, 'ether')

# Mendapatkan nonce untuk transaksi
def get_nonce(sender_address):
    return web3.eth.get_transaction_count(sender_address)

# Mengambil harga gas terkini
def get_gas_price():
    return web3.eth.gas_price

# Mengirim transaksi
def send_transaction(wallet, receiver_address, amount, gas_price):
    nonce = get_nonce(wallet['address'])
    sender_balance_before = get_balance(wallet['address'])
    print(Fore.BLUE + f"{BALANCE_SYMBOL} Saldo Pengirim Sebelum Tx: {sender_balance_before:.18f} {ETH_SYMBOL}")
    print(Fore.CYAN + f"{SENDER_ADDRESS_SYMBOL} {wallet['address']}")
    print(Fore.MAGENTA + f"{RECEIVER_ADDRESS_SYMBOL} {receiver_address}")
    print(Fore.LIGHTYELLOW_EX + f"{AMOUNT_SYMBOL} {amount:.18f} {ETH_SYMBOL}")

    tx = {
        'nonce': nonce,
        'to': receiver_address,
        'value': web3.to_wei(amount, 'ether'),
        'gas': 21000,
        'gasPrice': gas_price,
        'chainId': 1301
    }

    signed_tx = web3.eth.account.sign_transaction(tx, wallet['private_key'])

    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(Fore.CYAN + f"{datetime.now()} - Transaksi berhasil ke {receiver_address}. {CHECK_MARK}")
        
        sender_balance_after = get_balance(wallet['address'])
        print(Fore.YELLOW + f"{BALANCE_SYMBOL} Saldo Pengirim Setelah Tx: {sender_balance_after:.18f} {ETH_SYMBOL}")
        print(Fore.BLUE + f"{SENDER_ADDRESS_SYMBOL} {wallet['address']} {CHECK_MARK}")
        print(Fore.MAGENTA + f"{RECEIVER_ADDRESS_SYMBOL} {receiver_address} {CHECK_MARK}\n")

    except Exception as e:
        print(Fore.RED + f"Gagal mengirim transaksi: {str(e)} {CROSS_MARK}")

def countdown(seconds):
    while seconds:
        print(Fore.MAGENTA + f"Menunggu {seconds} detik untuk mencoba kembali...", end='\r')
        time.sleep(1)
        seconds -= 1
    print(Fore.GREEN + "Memulai kembali proses...\n")

# Pilihan menu interaktif
def menu():
    print(Fore.YELLOW + "=" * 50)
    print(Fore.CYAN + "1. Jalankan Bot")
    print(Fore.MAGENTA + "2. Tambah Wallet")
    print(Fore.YELLOW + "=" * 50)
    choice = input("Pilih opsi (1/2): ")

    if choice == "1":
        run_bot()
    elif choice == "2":
        add_wallet()
    else:
        print(Fore.RED + "Pilihan tidak valid. Silakan pilih 1 atau 2.")
        menu()

# Menjalankan bot
def run_bot():
    wallets = load_wallets()

    if not wallets:
        print(Fore.RED + "Tidak ada wallet yang tersedia. Silakan tambahkan wallet terlebih dahulu.")
        menu()
        return

    # Variabel untuk menghitung transaksi dan melacak tanggal saat ini
    transaction_count = 0
    current_date = datetime.now().date()
    daily_transaction_limit = random.randint(400, 450)  # Acak jumlah transaksi harian, minimal 400

    while True:
        print_header()

        # Periksa apakah tanggal sudah berubah
        if datetime.now().date() != current_date:
            current_date = datetime.now().date()  # Reset tanggal
            transaction_count = 0  # Reset jumlah transaksi
            daily_transaction_limit = random.randint(400, 450)  # Tentukan batas harian baru

        # Cek apakah sudah mencapai batas transaksi harian
        if transaction_count >= daily_transaction_limit:
            next_day = current_date + timedelta(days=1)
            remaining_time = (datetime.combine(next_day, datetime.min.time()) - datetime.now()).total_seconds()
            print(Fore.RED + f"Mencapai batas transaksi harian ({daily_transaction_limit}). Menunggu hingga {next_day}...")
            countdown(int(remaining_time))
            current_date = datetime.now().date()
            transaction_count = 0  # Reset jumlah transaksi setelah menunggu
            daily_transaction_limit = random.randint(400, 450)  # Tentukan batas harian baru
            continue

        # Pilih wallet secara acak
        wallet = random.choice(wallets)

        # Transaksi
        receiver = generate_random_address()
        random_amount = random.uniform(0.00000001, 0.00000002)  # Jumlah pengiriman tetap kecil
        gas_price = get_gas_price()
        send_transaction(wallet, receiver, random_amount, gas_price)

        transaction_count += 1  # Tambahkan transaksi ke hitungan

        # Tunggu dengan jeda acak antara 30 hingga 60 detik
        countdown(random.randint(30, 60))

# Menjalankan menu
menu()

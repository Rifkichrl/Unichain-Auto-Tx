# Unichain Auto SOLO/MULTI WALLET Transaction Bot

Skrip ini digunakan untuk melakukan transaksi otomatis di jaringan **Unichain Sepolia** dengan pengaturan fleksibel seperti jumlah transaksi acak, jeda waktu acak, dan batas transaksi harian.

## Cara Menggunakan

### 1. Clone Repositori
Clone repositori ini ke mesin lokal Anda:
```bash
git clone https://github.com/Rifkichrl/Unichain-Auto-Tx.git
```

### 2. Masuk ke Folder Proyek
Gunakan perintah berikut untuk masuk ke folder:
```bash
cd Unichain-Auto-Tx
```

### 3. Install Dependencies
Install dependencies yang diperlukan:
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi
Buka file `.env` di folder proyek dengan cara : 
```
sudo nano .env 
```
dan tambahkan konfigurasi berikut:
```env
SENDER_ADDRESS=PASTE_ALAMAT_WALLET
PRIVATE_KEY=PASTE_PRIVATE_KEY_KAMU
```
Ganti `PASTE_ALAMAT_WALLET` dengan alamat wallet Anda dan `PASTE_PRIVATE_KEY_KAMU` dengan private key wallet Anda.

### 5. Jalankan Script
Jalankan skrip dengan perintah:
```bash
python3 unichain_sepolia.py
```

---

## Panduan Penggunaan di TERMUX

Jika Anda menggunakan Termux dan menghadapi kendala, ikuti langkah-langkah berikut:

### 1. Instalasi Proot dan Ubuntu
Masuk ke mode **proot distro Ubuntu**:
```bash
pkg install proot
pkg install openssh
pkg install git
curl -L -o proot_5.1.107-52_aarch64.deb https://github.com/SukunDev/termux-proot/raw/main/proot_5.1.107-52_aarch64.deb
dpkg -i proot_5.1.107-52_aarch64.deb
pkg install -y proot-distro
proot-distro install ubuntu
proot-distro login ubuntu
```

### 2. Konfigurasi Python dan Virtual Environment
Setelah masuk ke Ubuntu, lakukan konfigurasi berikut:
```bash
apt update && apt upgrade
apt install python3-pip
pip install --upgrade pip==24.2
apt install python3-venv
python3 -m venv myenv
source myenv/bin/activate
pip install --upgrade pip setuptools
```
(Jika diminta memilih zona waktu, pilih angka **5** untuk Asia dan **35** untuk waktu area Jakarta, lalu ikuti instruksi dengan menekan `y` dan `Enter`.)

### 3. Clone Proyek di Ubuntu
Clone repositori ini di lingkungan Ubuntu:
```bash
git clone https://github.com/Rifkichrl/Unichain-Auto-Tx.git
cd Unichain-Auto-Tx
pip install -r requirements.txt
```

### 4. Konfigurasi dan Jalankan
Lakukan konfigurasi `.env` seperti di atas, lalu jalankan script dengan:
```bash
python3 unichain_sepolia.py
```

---

## Catatan Tambahan
- multi.py digunakan untuk transaksi banyak wallet serta bisa generate new wallet juga
- load.py digunakan untuk menyimpan alamat wallet baru yang di generate ke wallet.txt (digunakan untuk mengirim saldo dari bot unichain_sepolia.py)
- unichain_sepolia.py akan mengirim terlebih dahulu ke alamat prioritas yaitu ke alamat yang di simpan di wallet.txt , jika tidak ada maka akan mengirim ke random alamat
- Pastikan Anda memiliki koneksi internet yang stabil.
- Jika ada masalah, silakan cek dokumentasi tambahan yang tersedia di setiap file atau repositori ini.

Selamat menggunakan! 🚀
```
traktiran nya dong abangku
```

import csv
import os
from datetime import datetime
from collections import defaultdict

# ============================== Data Storage ==============================

produk_file = 'produk.csv'
transaksi_file = 'transaksi.csv'

def load_produk():
    produk = {}
    if os.path.exists(produk_file):
        with open(produk_file, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                produk[row['id']] = {
                    'nama': row['nama'],
                    'harga': int(row['harga']),
                    'stok': int(row['stok']),
                    'deskripsi': row['deskripsi']
                }
    return produk

def simpan_produk(produk):
    with open(produk_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'nama', 'harga', 'stok', 'deskripsi'])
        writer.writeheader()
        for id, data in produk.items():
            row = {'id': id, **data}
            writer.writerow(row)

def tambah_transaksi(id_produk, jumlah, tipe):
    now = datetime.now()
    tanggal = now.strftime('%Y-%m-%d')
    waktu = now.strftime('%H:%M:%S')
    with open(transaksi_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if os.stat(transaksi_file).st_size == 0:
            writer.writerow(['tanggal', 'waktu', 'id_produk', 'jumlah', 'tipe'])
        writer.writerow([tanggal, waktu, id_produk, jumlah, tipe])

def load_transaksi():
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    if os.path.exists(transaksi_file):
        with open(transaksi_file, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tgl = datetime.strptime(row['tanggal'], '%Y-%m-%d')
                year, month, day = tgl.year, tgl.month, tgl.day
                tree[year][month][day].append(row)
    return tree

# ============================== Produk ==============================

def kelola_produk(produk):
    while True:
        print("\n--- Kelola Produk ---")
        print("1. Tambah Produk")
        print("2. Lihat Produk")
        print("3. Ubah Produk")
        print("4. Hapus Produk")
        print("5. Kembali")
        pilih = input("Pilih: ")

        if pilih == '1':
            id = input("ID Produk: ")
            if id in produk:
                print("ID sudah ada.")
                continue
            nama = input("Nama Produk: ")
            harga = int(input("Harga: "))
            stok = int(input("Stok: "))
            deskripsi = input("Deskripsi: ")
            produk[id] = {'nama': nama, 'harga': harga, 'stok': stok, 'deskripsi': deskripsi}
            simpan_produk(produk)
            print("Produk berhasil ditambahkan.")
        elif pilih == '2':
            if not produk:
                print("Tidak ada produk.")
            for id, data in produk.items():
                print(f"ID: {id} | Nama: {data['nama']} | Harga: {data['harga']} | Stok: {data['stok']} | Deskripsi: {data['deskripsi']}")
        elif pilih == '3':
            id = input("ID Produk yang ingin diubah: ")
            if id not in produk:
                print("Produk tidak ditemukan.")
                continue
            nama = input("Nama Baru: ")
            harga = int(input("Harga Baru: "))
            stok = int(input("Stok Baru: "))
            deskripsi = input("Deskripsi Baru: ")
            produk[id] = {'nama': nama, 'harga': harga, 'stok': stok, 'deskripsi': deskripsi}
            simpan_produk(produk)
            print("Produk berhasil diubah.")
        elif pilih == '4':
            id = input("ID Produk yang ingin dihapus: ")
            if id in produk:
                del produk[id]
                simpan_produk(produk)
                print("Produk dihapus.")
            else:
                print("Produk tidak ditemukan.")
        elif pilih == '5':
            break
        else:
            print("Pilihan tidak valid.")

# ============================== Transaksi ==============================

def transaksi(produk):
    print("\n--- Transaksi ---")
    id = input("ID Produk: ")
    if id not in produk:
        print("Produk tidak ditemukan.")
        return
    tipe = input("Jenis (penjualan/pembelian): ").lower()
    if tipe not in ['penjualan', 'pembelian']:
        print("Jenis tidak valid.")
        return
    jumlah = int(input("Jumlah: "))
    if tipe == 'penjualan':
        if produk[id]['stok'] < jumlah:
            print("Stok tidak cukup.")
            return
        produk[id]['stok'] -= jumlah
    else:
        produk[id]['stok'] += jumlah
    simpan_produk(produk)
    tambah_transaksi(id, jumlah, tipe)
    print(f"Transaksi {tipe} berhasil.")

# ============================== Laporan ==============================

def laporan():
    tree = load_transaksi()
    print("\n--- Laporan Penjualan ---")
    print("1. Harian")
    print("2. Mingguan")
    print("3. Bulanan")
    pilih = input("Pilih: ")

    now = datetime.now()
    y, m, d = now.year, now.month, now.day

    if pilih == '1':
        laporan_harian(tree, y, m, d)
    elif pilih == '2':
        laporan_mingguan(tree, y, m, d)
    elif pilih == '3':
        laporan_bulanan(tree, y, m)
    else:
        print("Pilihan tidak valid.")

def laporan_harian(tree, y, m, d):
    print(f"\nLaporan Harian {y}-{m:02d}-{d:02d}")
    data = tree[y][m][d]
    if not data:
        print("Tidak ada transaksi.")
        return
    for t in data:
        print(t)

def laporan_mingguan(tree, y, m, d):
    print(f"\nLaporan Mingguan {y}-{m:02d}, sekitar hari {d}")
    found = False
    for day in range(d-3, d+4):
        if day < 1 or day > 31:
            continue
        for t in tree[y][m][day]:
            print(t)
            found = True
    if not found:
        print("Tidak ada transaksi.")

def laporan_bulanan(tree, y, m):
    print(f"\nLaporan Bulanan {y}-{m:02d}")
    found = False
    for day in tree[y][m]:
        for t in tree[y][m][day]:
            print(t)
            found = True
    if not found:
        print("Tidak ada transaksi.")

# ============================== Main Program ==============================

def main():
    produk = load_produk()
    while True:
        print("\n=== Menu Utama ===")
        print("1. Kelola Produk")
        print("2. Transaksi")
        print("3. Laporan")
        print("4. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            kelola_produk(produk)
        elif pilihan == '2':
            transaksi(produk)
        elif pilihan == '3':
            laporan()
        elif pilihan == '4':
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()

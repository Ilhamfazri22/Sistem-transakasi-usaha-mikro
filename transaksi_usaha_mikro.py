import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import csv
from collections import deque

# Struktur Data
produk_list = []
transaksi_queue = deque()

# Load data dari CSV
def load_data():
    try:
        with open('produk.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['harga'] = float(row['harga'])
                row['stok'] = int(row['stok'])
                produk_list.append(row)
    except FileNotFoundError:
        pass

# Simpan ke CSV
def simpan_data():
    with open('produk.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['nama', 'harga', 'stok'])
        writer.writeheader()
        writer.writerows(produk_list)

# Tambah Produk
def tambah_produk():
    nama = simpledialog.askstring("Input", "Nama produk:")
    harga = simpledialog.askfloat("Input", "Harga:")
    stok = simpledialog.askinteger("Input", "Stok:")

    if nama and harga is not None and stok is not None:
        produk_list.append({'nama': nama, 'harga': harga, 'stok': stok})
        simpan_data()
        messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")

# Lihat Produk dengan Treeview dan scrollbar
def lihat_produk():
    win = tk.Toplevel(root)
    win.title("Daftar Produk")
    win.configure(bg="#f0f0f0")
    frame = tk.Frame(win, bg="#f0f0f0")
    frame.pack(padx=10, pady=10)

    # Scrollbar
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Treeview (Tabel)
    tree = ttk.Treeview(frame, columns=("Nama", "Harga", "Stok"), show="headings", yscrollcommand=scrollbar.set)
    
    # Definisikan kolom
    tree.heading("Nama", text="Nama Produk", anchor="center")
    tree.heading("Harga", text="Harga", anchor="center")
    tree.heading("Stok", text="Stok", anchor="center")

    tree.column("Nama", width=200, anchor="center")
    tree.column("Harga", width=100, anchor="center")
    tree.column("Stok", width=80, anchor="center")

    # Masukkan data produk
    for p in produk_list:
        tree.insert("", "end", values=(p['nama'], f"Rp{p['harga']:,}", p['stok']))

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=tree.yview)

# Tambah Transaksi (Penjualan/Pembelian)
def tambah_transaksi(tipe):
    nama_produk = simpledialog.askstring("Input", "Nama produk:")
    jumlah = simpledialog.askinteger("Input", "Jumlah:")
    if not nama_produk or jumlah is None:
        return

    for p in produk_list:
        if p['nama'].lower() == nama_produk.lower():
            transaksi_queue.append({'tipe': tipe, 'produk': p, 'jumlah': jumlah})
            messagebox.showinfo("Sukses", f"Transaksi {tipe} ditambahkan ke antrian.")
            return
    messagebox.showerror("Error", "Produk tidak ditemukan!")

# Proses Transaksi
def proses_transaksi():
    if not transaksi_queue:
        messagebox.showinfo("Info", "Tidak ada transaksi dalam antrian.")
        return

    transaksi = transaksi_queue.popleft()
    produk = transaksi['produk']
    jumlah = transaksi['jumlah']
    tipe = transaksi['tipe']

    if tipe == 'Penjualan':
        if produk['stok'] >= jumlah:
            produk['stok'] -= jumlah
            messagebox.showinfo("Sukses", f"Transaksi penjualan {jumlah} unit {produk['nama']} diproses.")
        else:
            messagebox.showerror("Gagal", "Stok tidak cukup!")
            return
    elif tipe == 'Pembelian':
        produk['stok'] += jumlah
        messagebox.showinfo("Sukses", f"Transaksi pembelian {jumlah} unit {produk['nama']} diproses.")

    simpan_data()

# Lihat Antrian Transaksi
def lihat_antrian():
    win = tk.Toplevel(root)
    win.title("Antrian Transaksi")
    win.configure(bg="#f0f0f0")
    frame = tk.Frame(win, bg="#f0f0f0")
    frame.pack(padx=10, pady=10)

    # Scrollbar
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Treeview (Tabel) untuk antrian transaksi
    tree = ttk.Treeview(frame, columns=("Tipe", "Produk", "Jumlah"), show="headings", yscrollcommand=scrollbar.set)
    
    # Definisikan kolom
    tree.heading("Tipe", text="Tipe Transaksi", anchor="center")
    tree.heading("Produk", text="Nama Produk", anchor="center")
    tree.heading("Jumlah", text="Jumlah", anchor="center")

    tree.column("Tipe", width=150, anchor="center")
    tree.column("Produk", width=200, anchor="center")
    tree.column("Jumlah", width=100, anchor="center")

    # Masukkan data transaksi yang ada dalam antrian
    for transaksi in transaksi_queue:
        tree.insert("", "end", values=(transaksi['tipe'], transaksi['produk']['nama'], transaksi['jumlah']))

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=tree.yview)

# GUI
root = tk.Tk()
root.title("Sistem Transaksi Usaha Mikro")
root.configure(bg="#e0f7fa")

judul = tk.Label(root, text="Sistem Transaksi Usaha Mikro", font=("Segoe UI", 16, "bold"), bg="#e0f7fa", fg="#00796b")
judul.pack(pady=(15, 10))

button_style = {"font": ("Segoe UI", 11), "bg": "#4dd0e1", "fg": "#fff", "activebackground": "#0097a7", "activeforeground": "#fff", "bd": 0}

tk.Button(root, text="➕ Tambah Produk", width=30, command=tambah_produk, **button_style).pack(pady=5)
tk.Button(root, text="📄 Lihat Daftar Produk", width=30, command=lihat_produk, **button_style).pack(pady=5)
tk.Button(root, text="🛒 Tambah Transaksi Penjualan", width=30, command=lambda: tambah_transaksi('Penjualan'), **button_style).pack(pady=5)
tk.Button(root, text="📥 Tambah Transaksi Pembelian", width=30, command=lambda: tambah_transaksi('Pembelian'), **button_style).pack(pady=5)
tk.Button(root, text="⚙️ Proses Transaksi", width=30, command=proses_transaksi, **button_style).pack(pady=5)
tk.Button(root, text="📜 Lihat Antrian Transaksi", width=30, command=lihat_antrian, **button_style).pack(pady=5)
tk.Button(root, text="❌ Keluar", width=30, command=root.quit, **button_style).pack(pady=(5, 15))

load_data()
root.mainloop()

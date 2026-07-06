# Dataset

Letakkan file dataset **Online Retail** di folder ini dengan nama `online_retail.xlsx` (atau `.csv`).

Dataset standar yang dipakai di banyak studi kasus RFM:
- **UCI Machine Learning Repository** — "Online Retail" (ID 352): https://archive.ics.uci.edu/dataset/352/online+retail
- Atau cari di Kaggle dengan kata kunci **"Online Retail Dataset UCI"**.

Kolom yang diharapkan ada:
| Kolom | Deskripsi |
|---|---|
| InvoiceNo | Nomor invoice (6 digit). Jika diawali huruf 'C' -> transaksi cancel/retur |
| StockCode | Kode produk |
| Description | Nama produk |
| Quantity | Jumlah unit per baris transaksi |
| InvoiceDate | Tanggal & waktu transaksi |
| UnitPrice | Harga per unit |
| CustomerID | ID pelanggan (banyak yang kosong -> guest checkout) |
| Country | Negara pelanggan |

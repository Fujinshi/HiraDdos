
# 🌌 HiraDdos 🌌

[![GitHub Release](https://img.shields.io/github/v/release/Fujinshi/HiraDdos)](https://github.com/Fujinshi/HiraDdos/releases)
[![GitHub Stars](https://img.shields.io/github/stars/Fujinshi/HiraDdos)](https://github.com/Fujinshi/HiraDdos/stargazers)
[![GitHub License](https://img.shields.io/github/license/Fujinshi/HiraDdos)](https://github.com/Fujinshi/HiraDdos/blob/master/LICENSE)

**HiraDdos** adalah sebuah *advanced stress testing tool* yang dirancang untuk menguji ketahanan server dan infrastruktur jaringan terhadap serangan volumetrik. Dibangun dengan konsep **High-Performance Network Stresser**, HiraDdos memberikan kekuatan penuh dalam genggaman Anda dengan tampilan antarmuka CLI yang tetap membawa semangat **Dark Neon Aesthetic**.

> **Peringatan:** Alat ini dibuat murni untuk tujuan edukasi, riset keamanan, dan pengujian beban sistem (load testing) yang legal. Penyalahgunaan alat ini untuk aktivitas ilegal di luar izin pemilik target sepenuhnya merupakan tanggung jawab pengguna.

---

## ⚡ Fitur Utama

HiraDdos dioptimalkan untuk memberikan *throughput* maksimal dengan berbagai metode:

**🌐 Layer 7 (Application Layer)**
*   **HTTP/2 Flood:** Menggunakan protokol HTTP terbaru untuk efisiensi serangan tinggi.
*   **Headless Browser Attack:** Mensimulasikan trafik manusia yang nyata untuk melewati sistem filter dasar.
*   **Proxy Rotator:** Dukungan otomatis untuk ribuan proxy guna menjaga anonimitas serangan.

**🛡️ Layer 4 (Transport Layer)**
*   **UDP/TCP Flood:** Serangan langsung ke port protokol untuk menguras *bandwidth* target.
*   **Syn Flood:** Teknik klasik yang dioptimalkan untuk membanjiri antrean koneksi server.

**⚙️ Optimasi Performa**
*   **Multithreading Engine:** Memanfaatkan seluruh core CPU untuk memproses paket data secara simultan.
*   **Auto-Update Proxy:** Mengambil list proxy segar secara otomatis dari sumber terpercaya.
*   **Real-time Stats:** Monitor jumlah *request* yang terkirim secara langsung melalui terminal.

---

## 📸 Antarmuka

| Dashboard Utama | Eksekusi Serangan | Monitoring |
|:---:|:---:|:---:|
| *(Tampilan menu neon)* | *(Proses pengiriman paket)* | *(Statistik trafik keluar)* |

> **Visual:** Antarmuka HiraDdos menggunakan skema warna **Neon Purple & Cyan** untuk memudahkan pembacaan log saat proses *testing* berlangsung.

---

## 📥 Panduan Instalasi

Pastikan sistem Anda sudah terpasang **Python 3.9+**.

1.  **Clone Repository:**
    ```bash
    git clone [https://github.com/Fujinshi/HiraDdos.git](https://github.com/Fujinshi/HiraDdos.git)
    cd HiraDdos
    ```
2.  **Install Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Jalankan Tools:**
    ```bash
    python hira.py
    ```

---

## 👥 Developer

Proyek ini dikembangkan dan dirawat oleh:

*   **HiraKoxs** - Lead Developer
    *   [![Telegram](https://img.shields.io/badge/Telegram-@hirakox-blue?style=flat-square&logo=telegram)](https://t.me/hirakox)

Terima kasih kepada seluruh rekan-rekan *cybersecurity enthusiast* yang telah memberikan feedback untuk optimasi script ini.

---

## 💬 Hubungi Kami

Jika Anda menemukan kendala teknis atau ingin memberikan saran fitur:

*   📱 **Telegram Official:** [https://t.me/hirakox](https://t.me/hirakox)
*   🚩 **Bug Report:** Silakan buka [GitHub Issues](https://github.com/Fujinshi/HiraDdos/issues).

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah **GNU General Public License v3.0**. Lihat file `LICENSE` untuk informasi lebih lanjut.

---

**✨ HiraDdos - Uji batas ketahanan sistem Anda sekarang! ✨**

```markdown
<div align="center">
  
  # ⚡ HIRAKO DDOS SYSTEM ⚡
  
  ### *Ultimate DDoS Tool with Proxy Rotator & Multi-Strategy Attacks*
  
  ![Version](https://img.shields.io/badge/version-4.0-red)
  ![Python](https://img.shields.io/badge/python-3.8+-blue)
  ![License](https://img.shields.io/badge/license-MIT-green)
  ![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20Termux-lightgrey)
  
```

---

| | | () __ __ _| | _____   |  _ \  __| | ___  ___

| || | | '__/  | |/ / _ \  | | | |/ _ |/ _ \/ __|
|  _  | | | | (| |   < () | | || | (| | () \__ 
  || ||||  \_,||\_\___/  |___/ \_,|\_/|/

```
  
  ### *"Gas terus, kontol!" - Hirakox*
  
  [![Telegram](https://img.shields.io/badge/Contact-Developer-2CA5E0?style=for-the-badge&logo=telegram)](https://t.me/hirakox)
  [![GitHub](https://img.shields.io/badge/Star-this%20repo-ff69b4?style=for-the-badge&logo=github)](https://github.com/Fujinshi/HiraDdos)
  
</div>

---

## 🔥 **Fitur SUPER GANAS**

| Fitur | Status | Deskripsi |
|-------|--------|------------|
| 🌀 **Multi Proxy Support** | ✅ | HTTP, HTTPS, SOCKS4, SOCKS5 |
| 🔄 **Proxy Rotator** | ✅ | Auto-rotate dari GitHub |
| 💣 **6 Attack Strategies** | ✅ | Mixed, HTTP, Slowloris, Amplification, Pipeline, TCP, UDP |
| ⚡ **Intensity Level** | ✅ | Normal, High, Extreme |
| 🎯 **Live Proxy Monitoring** | ✅ | Lihat proxy yang dipake realtime |
| 📡 **Amplification Attack** | ✅ | DNS, NTP, Memcached, SSDP |
| 🐌 **Slowloris** | ✅ | Bikin server kehabisan koneksi |
| 🚀 **HTTP Pipelining** | ✅ | Multiple request 1 koneksi |
| 📊 **Real-time Stats** | ✅ | Packet, Success, Failed, Bytes |
| 💾 **Auto Logging** | ✅ | Download hasil serangan |
| 🧵 **Multi-threading** | ✅ | Sampai 1000+ threads |

---

## 🛠️ **Installasi**

### 📌 **Termux (Android)**
```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/Fujinshi/HiraDdos.git
cd HiraDdos
pip install -r requirements.txt
python main.py
```

💻 Linux / VPS

```bash
sudo apt update
sudo apt install python3 python3-pip git
git clone https://github.com/Fujinshi/HiraDdos.git
cd HiraDdos
pip3 install -r requirements.txt
python3 main.py
```

🪟 Windows

```powershell
git clone https://github.com/Fujinshi/HiraDdos.git
cd HiraDdos
pip install -r requirements.txt
python main.py
```

---

🚀 Cara Pemakaian

1. Jalankan Server

```bash
python main.py
```

Server akan berjalan di http://localhost:8080

2. Buka Browser

Akses http://localhost:8080 atau http://[IP-VPS]:8080

3. Set Parameter Attack

Parameter Opsi Keterangan
Target example.com Domain atau IP target
Port 80, 443, 8080 Kosongin kalo HTTP/HTTPS
Attack Type HTTP/TCP/UDP Jenis serangan dasar
Strategy Mixed, Slowloris, dll Mode serangan cerdas
Intensity Normal/High/Extreme Seberapa ganas
Concurrency 50-1000 Jumlah thread
Proxy YES/NO Pake proxy rotator atau enggak

4. Tombol Gas ⚡

Klik "INITIATE ATTACK" dan lihat target nyungsep!

---

🎮 Attack Strategies Explained

Strategy Cara Kerja Efek
MIXED Auto-rotate semua strategy Susah di-detect
HTTP Flood Request HTTP normal Consume bandwidth
Slowloris Keep connections hanging Habisin koneksi server
Amplification UDP spoofing ke resolver 50-100x bandwidth
Pipeline HTTP/1.1 pipelining Beban server berat
TCP Flood Raw TCP packets Habisin koneksi
UDP Flood Random UDP packets Beban firewall

---

📸 Screenshot

```
┌─────────────────────────────────────────────────────────┐
│  _   _ _           _           ____      _              │
│ | | | (_)_ __ __ _| | _____   |  _ \  __| | ___  ___    │
│ | |_| | | '__/ _` | |/ / _ \  | | | |/ _` |/ _ \/ __|   │
│ |  _  | | | | (_| |   < (_) | | |_| | (_| | (_) \__ \   │
│ |_| |_|_|_|  \__,_|_|\_\___/  |____/ \__,_|\___/|___/   │
│                                                          │
│  [+] Loaded 487 HTTP proxies                            │
│  [+] Loaded 234 HTTPS proxies                           │
│  [+] Loaded 156 SOCKS4 proxies                          │
│  [+] Loaded 892 SOCKS5 proxies                          │
│  [+] Total proxies loaded: 1769                         │
│                                                          │
│  [*] Server running on http://0.0.0.0:8080              │
└─────────────────────────────────────────────────────────┘
```

---

🔧 Requirements

```txt
Flask==2.3.2
flask-cors==4.0.0
requests==2.31.0
PySocks==1.7.1
urllib3==2.0.4
```

Install semua pake:

```bash
pip install -r requirements.txt
```

---

⚠️ DISCLAIMER

```
╔══════════════════════════════════════════════════════════╗
║  TOOL INI UNTUK EDUCATIONAL PURPOSE & SECURITY TESTING  ║
║                                                          ║
║  - Hanya gunakan di sistem yang lo miliki               ║
║  - Dapat izin SEBELUM testing                            ║
║  - Developer tidak bertanggung jawab atas penyalahgunaan║
║  - Illegal use = tanggung sendiri gan!                  ║
╚══════════════════════════════════════════════════════════╝
```

---

📞 Contact Developer

<div align="center">

https://img.shields.io/badge/Telegram-@hirakox-2CA5E0?style=for-the-badge&logo=telegram
https://img.shields.io/badge/GitHub-Fujinshi-181717?style=for-the-badge&logo=github

"Mau bot? PM ane. Gas terus!" 🔥

</div>

---

🌟 Support Project

Like dan fork repo ini kalo berguna:

```bash
git clone https://github.com/Fujinshi/HiraDdos.git
cd HiraDdos
python main.py
# Kalo suka kasih ⭐ ya kontol!
```

---

<div align="center">

© 2026 HIRAKO SYSTEMS | Made with 🖤 by @hirakox

"Jangan lupa solat, tapi serangan jangan sampe putus!" 💀

</div>
```

# IMSI Catcher

This application is designed to monitor and record IMSI (International Mobile Subscriber Identity) from BTS logs (e.g., OpenBTS/YateBTS) locally using FastAPI.

## 📦 Features
- Store IMSI data from BTS logs
- REST API endpoints to view and add IMSI
- Uses SQLite for local storage
- Runs well on Raspberry Pi 4 + Ubuntu 22.04

## 🧰 System Requirements

### 🎯 Hardware:
- Raspberry Pi 4 (4GB or 8GB RAM recommended)
- HackRF One
- Dummy SIM or old phone for connection simulation
- (Optional) Faraday cage for signal isolation

### 🧪 Software:
| Tool             | Function                                |
|------------------|------------------------------------------|
| HackRF Tools     | Control and test HackRF                 |
| OpenBTS/YateBTS  | GSM BTS emulation                      |
| GNU Radio        | SDR processing (modulation backend)    |
| Python 3.10+     | Backend for FastAPI                     |
| FastAPI          | REST API framework                      |
| SQLite3          | Local IMSI storage                      |
| Uvicorn          | Web server for FastAPI                  |

## 🚀 Installation & Setup Steps

### 🔹 1. Install Dependencies
```bash
sudo apt update && sudo apt install -y \
  python3 python3-pip python3-venv sqlite3 \
  git build-essential cmake \
  gnuradio hackrf libhackrf-dev \
  net-tools
```

> Check if HackRF is detected:
```bash
hackrf_info
```

### 🔹 2. Install YateBTS (Optional)
```bash
sudo apt install yate yate-common yate-qt4 yate-server yate-bts
sudo yate -s
```

### 🔹 3. Set Up IMSI Catcher Project
```bash
git clone https://github.com/yourname/imsicatcher.git
cd imsicatcher
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🔹 4. Run FastAPI
```bash
bash run.sh
```

Open your browser: [http://localhost:8000/docs](http://localhost:8000/docs)

### 🔹 5. IMSI Simulation (Manual Testing)
Manually add IMSI log for testing:
```bash
echo "[OpenBTS] IMSI 510010123456789 detected at signal -72dB" >> logs/openbts.log
```
Then access:
```bash
curl http://localhost:8000/imsi
```

## 📁 Directory Structure
- `app/`: Main FastAPI application code
- `logs/openbts.log`: Log file being monitored
- `imsicatcher.db`: Local SQLite database

## 🧪 Example Request
Manually add an IMSI:
```bash
curl -X POST http://localhost:8000/imsi \
 -H "Content-Type: application/json" \
 -d '{"imsi": "510010123456789", "timestamp": "2025-07-05T13:00:00"}'
```

## ⚠️ Legal & Ethical Notes
This application is for educational and private simulation purposes only.

Prohibited:
- Broadcasting BTS on public frequencies
- Using outside lab/private environments
- Capturing data without user consent

Use responsibly and comply with all applicable laws.

---

© 2025 - Cybersecurity Education | Que

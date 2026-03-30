# 🥊 VVN Combat - Hệ thống Chấm điểm Võ thuật Realtime

Hệ thống chấm điểm điện tử chuyên dụng cho các giải đấu võ thuật (Vovinam, Taekwondo, Kickboxing...), hỗ trợ tối đa 5 trọng tài chấm điểm đồng thời và hiển thị lịch sử khớp điểm thời gian thực.

---

## 🚀 Tính năng chính
- **Realtime Scoreboard**: Cập nhật điểm số ngay lập tức qua Socket.io.
- **Multi-Judge Support**: Hỗ trợ tối đa 5 trọng tài với định danh riêng (J1-J5).
- **Auto-Sync History**: Tự động lưu và hiển thị lịch sử chấm điểm vào Database sau mỗi 3 giây.
- **Admin Control**: Quản lý trận đấu, thời gian, thiết lập võ sĩ và kết thúc trận đấu.
- **Webhook Integration**: Tự động đẩy kết quả về hệ thống quản lý giải đấu trung tâm.

---

## 🛠 Cài đặt & Khởi chạy (Quick Start)

### 1. Yêu cầu hệ thống
- Máy tính cài sẵn **Python 3.11+**.
- Các thiết bị (Admin, Trọng tài) phải kết nối cùng một mạng nội bộ (Wi-Fi/LAN).

### 2. Cách khởi chạy nhanh (Mac/Linux)
1. Mở thư mục dự án trong Terminal.
2. Cấp quyền thực thi cho file chạy:
   ```bash
   chmod +x run.command
   ```
3. Click đúp vào file `run.command` hoặc chạy `./run.command`.

### 3. Truy cập giao diện
- **Admin**: `http://<IP_CUA_BAN>:5001/admin` (User: `admin` / Pass: `admin123`).
- **Trọng tài**: `http://<IP_CUA_BAN>:5001/` (Đăng nhập theo J1, J2... và ID trận đấu).

---

## 🌐 Chia sẻ trong mạng nội bộ
Để lấy địa chỉ IP gửi cho các trọng tài, gõ lệnh sau trong Terminal máy chủ:
```bash
ipconfig getifaddr en0
```
*(Link truy cập sẽ có dạng: `http://192.168.1.15:5001`)*

---

## 🔌 Tài liệu đấu nối API (Webhook Specification)

Hệ thống hỗ trợ gửi dữ liệu kết quả về máy chủ trung tâm thông qua Webhook sau khi nhấn nút **"Kết thúc"**.

### 1. Yêu cầu phía Hệ thống Tổng
Cung cấp một Webhook URL (Endpoint) tiếp nhận dữ liệu:
- **Phương thức**: `POST`
- **Xác thực**: Hỗ trợ `API-Key` hoặc `Bearer Token` trong Header.

### 2. Cấu trúc dữ liệu gửi đi (JSON Payload)
```json
{
  "match_id": "001",              // ID trận đấu lấy từ hệ thống của bạn
  "p1_name": "Võ sĩ Xanh",        // Tên võ sĩ 1 (Góc đài Xanh)
  "p2_name": "Võ sĩ Đỏ",          // Tên võ sĩ 2 (Góc đài Đỏ)
  "scores": {
    "p1_total": 15,               // Tổng điểm võ sĩ 1
    "p2_total": 10                // Tổng điểm võ sĩ 2
  },
  "outcome": {
    "winner_id": "p1",            // Định danh thắng cuộc (p1 hoặc p2)
    "result_type": "POINTS",      // Loại kết quả (POINTS, KO, TKO, DQ)
    "status": "COMPLETED"         // Trạng thái trận đấu
  },
  "timestamp": "2026-03-30 16:00:00"
}
```

### 3. Cấu hình phía V-Combat
Chỉnh sửa các biến sau trong file `app.py` để khớp với hệ thống của đối tác:
```python
WEBHOOK_URL = "https://tournament-system.com/api/v1/match-results"
HEADERS = {"Authorization": "Bearer YOUR_TOKEN_HERE"}
```

### 4. Phản hồi mong đợi (Response)
Hệ thống tổng cần trả về mã trạng thái thành công:
- **Success**: `HTTP 200 OK` hoặc `HTTP 201 Created`
- **Body**: `{"status": "success", "message": "Result updated"}`

---

## 📂 Cấu trúc thư mục dự án
```text
vvn/
├── app.py              # Xử lý Logic Server & SocketIO
├── combat.db           # Cơ sở dữ liệu SQLite lưu trữ lịch sử
├── run.command         # Script khởi chạy nhanh trên Mac
├── requirements.txt    # Danh sách thư viện cần thiết
└── templates/          # Giao diện HTML (Admin, Judge, Login)
```

---

## ⚠️ Lưu ý vận hành
1. **Clear Data**: Mỗi khi nhấn "Cập nhật" thông tin trận đấu mới, Database của `match_id` đó sẽ được làm sạch để bắt đầu chấm điểm lại từ đầu.
2. **Firewall**: Nếu trọng tài không truy cập được link IP, hãy kiểm tra và tắt Firewall trên máy chủ hoặc cho phép cổng `5001`.

@echo off
title VVN Combat Server - Windows
mode con: cols=65 lines=20
color 0B

echo ===========================================================
echo            HE THONG CHAM DIEM VVN COMBAT
echo ===========================================================
echo.

:: Tim dia chi IP IPv4 trong mang noi bo
set "IP="
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4" ^| findstr "192.168. 172. 10."') do (
    set "IP=%%a"
    goto :found
)

:found
if "%IP%"=="" (
    echo [!] KHONG TIM THAY IP! Kiem tra lai ket noi Wifi/LAN.
) else (
    set IP=%IP: =%
    echo  [OK] Server dang chay san sang!
    echo.
    echo  -----------------------------------------------------
    echo  DIA CHI TRUY CAP (Gui cho Trong tai):
    echo  Link: http://%IP%:5001
    echo  -----------------------------------------------------
    echo  QUAN LY (Dành cho Admin):
    echo  Link: http://localhost:5001/admin
    echo  -----------------------------------------------------
)

echo.
echo  [Ghi chu] Nhan Ctrl+C de dung server.
echo.
python app.py
pause


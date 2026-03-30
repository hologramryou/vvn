# 🥊 VVN Combat - Hệ thống Chấm điểm Võ thuật Realtime

Hệ thống chấm điểm điện tử chuyên dụng cho các giải đấu võ thuật (Vovinam, Taekwondo, Kickboxing...), hỗ trợ 5 trọng tài chấm điểm đồng thời và hiển thị lịch sử khớp điểm thời gian thực.

## 🚀 Tính năng chính
- **Realtime Scoreboard**: Cập nhật điểm số ngay lập tức qua Socket.io.
- **Multi-Judge Support**: Hỗ trợ tối đa 5 trọng tài với định danh riêng.
- **Auto-Sync History**: Tự động lưu và hiển thị lịch sử chấm điểm sau mỗi 3 giây.
- **Admin Control**: Quản lý trận đấu, thời gian, và thiết lập võ sĩ.
- **Portable**: Chạy trực tiếp trên macOS/Linux với script tự động.

## 🛠 Cài đặt nhanh (Quick Start)
1. **Yêu cầu**: Máy đã cài Python 3.11+.
2. **Thực thi**:
   - Chuột phải vào file `run.command` chọn **Open**.
   - Hoặc chạy lệnh: `./run.command` trong Terminal.
3. **Truy cập**:
   - **Admin**: `http://localhost:5001/admin` (User: `admin` / Pass: `admin123`)
   - **Trọng tài**: Truy cập qua IP máy chủ (Ví dụ: `http://192.168.1.15:5001`)

## 🌐 Chia sẻ trong mạng nội bộ
Để các trọng tài có thể truy cập bằng điện thoại:
1. Kết nối tất cả thiết bị vào cùng một mạng WiFi.
2. Lấy IP máy chủ (gõ `ifconfig` trong Terminal).
3. Chia sẻ link: `http://<IP_CUA_BAN>:5001`.

## 🔌 Tích hợp hệ thống (Tournament API)

Hệ thống hỗ trợ tự động gửi kết quả về máy chủ trung tâm (Hệ thống quản lý giải đấu) ngay khi nhấn **"KẾT THÚC"**.

### 1. Cấu hình Webhook
Mở file `app.py`, tìm hàm `send_result_to_server` và cập nhật các thông tin sau từ phía đối tác:
- `WEBHOOK_URL`: Địa chỉ nhận dữ liệu của hệ thống tổng.
- `HEADERS`: Token xác thực (nếu có).

### 2. Cấu trúc dữ liệu gửi đi (JSON Payload)
Khi trận đấu kết thúc, hệ thống sẽ gửi một yêu cầu `POST` với cấu trúc:

| Trường | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `match_id` | String | ID duy nhất của trận đấu |
| `p1_name` | String | Tên võ sĩ góc đài xanh |
| `p2_name` | String | Tên võ sĩ góc đài đỏ |
| `scores` | Object | Bao gồm `p1_total` và `p2_total` |
| `outcome` | Object | Kết quả (`winner_id`, `result_type`, `status`) |
| `timestamp`| String | Thời gian kết thúc trận đấu |

### 3. Phản hồi yêu cầu
Hệ thống tổng cần trả về mã trạng thái **HTTP 200** hoặc **201** để xác nhận đã nhận dữ liệu thành công. Mọi lỗi kết nối sẽ được ghi lại (Log) tại Terminal của máy chủ V-Combat.

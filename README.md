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
Hệ thống hỗ trợ gửi dữ liệu kết quả về máy chủ trung tâm thông qua Webhook hoặc API Call sau khi kết thúc trận đấu.

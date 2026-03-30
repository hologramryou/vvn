#!/bin/bash
echo "--- Đang khởi tạo hệ thống VVN Combat ---"

# Tạo môi trường ảo nếu chưa có
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Kích hoạt môi trường và cài thư viện
source venv/bin/activate
pip install -r requirements.txt

# Lấy địa chỉ IP nội bộ của máy Mac
IP_ADDR=$(ipconfig getifaddr en0)
if [ -z "$IP_ADDR" ]; then
    IP_ADDR=$(ipconfig getifaddr en1)
fi

echo "----------------------------------------"
echo "SERVER ĐANG CHẠY TẠI ĐỊA CHỈ:"
echo "http://$IP_ADDR:5001"
echo "----------------------------------------"

# Chạy ứng dụng
python3 app.py

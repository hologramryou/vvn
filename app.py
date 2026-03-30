import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, session, redirect, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vvn_ultimate_system_2024'
socketio = SocketIO(app, async_mode='eventlet')

# Khởi tạo Database
def init_db():
    with sqlite3.connect('combat.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS rounds 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      match_id TEXT, 
                      p1_name TEXT, 
                      p2_name TEXT, 
                      result TEXT, 
                      time TEXT)''')
        conn.commit()

# State quản lý trạng thái ứng dụng
state = {
    "match_id": "001",
    "p1": "Võ sĩ Xanh",
    "p2": "Võ sĩ Đỏ",
    "is_running": False,
    "voting_open": False,
    "current_votes": {},
    "allowed_judges": ["J1", "J2", "J3", "J4", "J5"]
}

@app.route('/')
def index():
    return render_template('login.html', state=state)

@app.route('/auth', methods=['POST'])
def auth():
    user = request.form.get('user')
    match_id_input = request.form.get('match_id')
    
    # Admin Login
    if user == "admin" and request.form.get('pass') == "admin123":
        session['user'], session['role'] = "admin", "admin"
        return redirect('/admin')
    
    # Judge Login
    if user in state['allowed_judges'] and match_id_input == state['match_id']:
        session['user'], session['role'] = user, "judge"
        return redirect('/judge')
        
    return "Sai thông tin đăng nhập! <a href='/'>Quay lại</a>"

@app.route('/admin')
def admin_page():
    if session.get('role') != 'admin': return redirect('/')
    return render_template('admin.html', state=state)

@app.route('/judge')
def judge_page():
    if session.get('role') != 'judge': return redirect('/')
    return render_template('judge.html', user=session['user'], state=state)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# API lấy lịch sử để tự động cập nhật bảng Admin
@app.route('/get_match_history/<match_id>')
def get_match_history(match_id):
    with sqlite3.connect('combat.db') as conn:
        c = conn.cursor()
        c.execute("SELECT result, time FROM rounds WHERE match_id=? ORDER BY id DESC", (match_id,))
        rows = c.fetchall()
        return jsonify([{"result": json.loads(r[0]), "time": r[1]} for r in rows])

# API tính tổng điểm cuối cùng
@app.route('/get_final_score/<match_id>')
def get_final_score(match_id):
    with sqlite3.connect('combat.db') as conn:
        c = conn.cursor()
        c.execute("SELECT result FROM rounds WHERE match_id=?", (match_id,))
        rows = c.fetchall()
        p1_total, p2_total = 0, 0
        for r in rows:
            votes = json.loads(r[0])
            for v in votes.values():
                if v['target'] == state['p1']: p1_total += v['pts']
                elif v['target'] == state['p2']: p2_total += v['pts']
        return jsonify({"p1": p1_total, "p2": p2_total})

# --- SOCKET.IO HANDLERS ---

@socketio.on('setup_match')
def setup_match(data):

    match_id = data['match_id']
    try:
        with sqlite3.connect('combat.db') as conn:
            conn.execute("DELETE FROM rounds WHERE match_id = ?", (match_id,))
            conn.commit()
        print(f"--- ĐÃ CLEAR TOÀN BỘ DB CỦA TRẬN: {match_id} ---")
    except Exception as e:
        print(f"Lỗi khi clear DB: {e}")
    # -----------------------------------------------
    state.update({
        "match_id": data['match_id'],
        "p1": data['p1'],
        "p2": data['p2'],
        "allowed_judges": data['judges'],
        "is_running": False,
        "voting_open": False,
        "current_votes": {}
    })
    emit('update_ui', state, broadcast=True)
    emit('match_status', {"is_running": False}, broadcast=True)

@socketio.on('toggle_match')
def toggle(data):
    state["is_running"] = data['status']
    emit('match_status', {"is_running": state["is_running"]}, broadcast=True)

@socketio.on('submit_point')
def handle_score(data):
    if not state["is_running"]: return
    judge = session.get('user')
    if not judge or judge not in state['allowed_judges']: return

    # Nếu bắt đầu một lượt chấm điểm mới (kích hoạt bởi người bấm đầu tiên)
    if not state["voting_open"]:
        state["voting_open"] = True
        state["current_votes"] = {} # Quan trọng: Reset bộ nhớ đệm điểm ngay lập tức
        
        # Gửi lệnh cho Admin xóa bảng Live Scoreboard ngay
        emit('clear_old_votes', broadcast=True)
        emit('start_3s_timer', {"duration": 3}, broadcast=True)
        socketio.start_background_task(close_window)

    # Cập nhật điểm của Judge vào bộ nhớ tạm
    state["current_votes"][judge] = {"target": data['target'], "pts": data['pts']}
    
    # Gửi đồng bộ liên tục cho Admin hiện lên Scoreboard
    emit('live_sync', state["current_votes"], broadcast=True)

def close_window():
    # Sử dụng socketio.sleep là đúng để không block server,
    # nhưng hãy đảm bảo state được lấy ra chuẩn xác
    socketio.sleep(3)
    
    state["voting_open"] = False
    
    # Copy dữ liệu ngay lập tức
    final_snapshot = dict(state["current_votes"])
    now_time = datetime.now().strftime("%H:%M:%S")

    if final_snapshot:
        res_str = json.dumps(final_snapshot)
        try:
            with sqlite3.connect('combat.db') as conn:
                conn.execute(
                    "INSERT INTO rounds (match_id, p1_name, p2_name, result, time) VALUES (?, ?, ?, ?, ?)",
                    (state['match_id'], state['p1'], state['p2'], res_str, now_time)
                )
                conn.commit()
            print(f"--- Đã lưu DB: {now_time} ---") # Log để bạn kiểm tra ở terminal
        except Exception as e:
            print(f"Lỗi DB: {e}")

    # GỬI DATA: Quan trọng là đặt bên ngoài IF để luôn có phản hồi về Admin
    print(f"--- Đang phát tín hiệu end_3s_timer tới Admin: {final_snapshot} ---")
    socketio.emit('end_3s_timer', {
        "result": final_snapshot,
        "time": now_time
    }) # namespace='/' nếu bạn có dùng namespace
    
    print(state["current_votes"])
    
    # Reset sau khi đã gửi xong
    state["current_votes"] = {}

@socketio.on('finish_match_event')
def handle_finish():
    state["is_running"] = False
    emit('force_logout', broadcast=True)

if __name__ == '__main__':
    init_db()
    # Chạy trên port 5001, cho phép truy cập từ mạng nội bộ (0.0.0.0)
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)

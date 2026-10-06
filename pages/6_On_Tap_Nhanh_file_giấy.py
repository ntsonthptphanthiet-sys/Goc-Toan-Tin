import streamlit as st
import pandas as pd
import random
import re # Thêm thư viện xử lý chuỗi

st.set_page_config(page_title="Ôn Tập Nhanh", page_icon="⚡")
st.title("⚡ Ôn Tập Nhanh: 10 Câu Trắc Nghiệm")

# --- 1. DÁN LINK GOOGLE SHEETS (CSV) CỦA ANH VÀO DÒNG DƯỚI NÀY ---
url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQJB3Xq8s1Xrs3BX-tUrLA92C8E9cnCRfhAuekiEitNCvC3WWeIoFhpm7INZ0Puhc-o6Md-DVeMcT1b/pub?output=csv"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        df = pd.read_csv(url)
        df = df.fillna("") 
        df['Phan'] = df['Phan'].astype(str).str.strip()
        df['DapAn'] = df['DapAn'].astype(str).str.replace(r'\.0$', '', regex=True)
        return df
    except Exception as e:
        return None

df = load_data(url_csv)
if df is None:
    st.error("⚠️ Lỗi tải dữ liệu. Anh Sơn kiểm tra lại link CSV nhé!")
    st.stop()

# HÀM LỌC TIỀN TỐ (Xóa A., B., C., D. ở đầu câu)
def clean_prefix(text):
    return re.sub(r'^[A-D][\.\)]\s*', '', str(text)).strip()

# --- 2. BỐC NGẪU NHIÊN 10 CÂU & TRỘN ĐÁP ÁN ---
if 'on_tap_10' not in st.session_state:
    p1_all = df[df['Phan'] == '1'].to_dict('records')
    so_cau = min(10, len(p1_all))
    p1_random = random.sample(p1_all, so_cau)
    
    p1_opts = {}
    for i, q in enumerate(p1_random):
        # Lột bỏ A, B, C, D cũ trong Excel
        opts = [clean_prefix(q['A']), clean_prefix(q['B']), clean_prefix(q['C']), clean_prefix(q['D'])]
        random.shuffle(opts) # Trộn nội dung
        
        # Gắn lại A, B, C, D mới cho đẹp đội hình
        p1_opts[i] = [f"A. {opts[0]}", f"B. {opts[1]}", f"C. {opts[2]}", f"D. {opts[3]}"]
        
    st.session_state.on_tap_10 = p1_random
    st.session_state.on_tap_opts = p1_opts

# --- 3. GIAO DIỆN LÀM BÀI TRỰC TUYẾN ---
st.info("🎯 Hệ thống đã bốc ngẫu nhiên 10 câu từ ngân hàng đề. Chúc em làm bài tốt!")

with st.form("mini_test"):
    luu_bai = {}
    for i, q in enumerate(st.session_state.on_tap_10):
        options = st.session_state.on_tap_opts[i]
        luu_bai[i] = st.radio(f"**Câu {i+1}:** {q['CauHoi']}", options, index=None, key=f"cau_{i}")
        st.markdown("---")
        
    nop_bai = st.form_submit_button("✅ Nộp bài & Xem điểm")
    
# --- 4. CHẤM ĐIỂM & LÀM LẠI ---
if nop_bai:
    so_cau_dung = 0
    for i, q in enumerate(st.session_state.on_tap_10):
        da_hs = str(luu_bai.get(i))
        da_chuan = str(q['DapAn'])
        
        # Lúc chấm điểm, lột bỏ chữ A,B,C,D đi, chỉ so sánh nội dung lõi với nhau
        if clean_prefix(da_hs) == clean_prefix(da_chuan) and da_hs != "None":
            so_cau_dung += 1
            
    st.success(f"🎉 Em làm đúng **{so_cau_dung} / {len(st.session_state.on_tap_10)}** câu!")
    st.metric("Điểm hệ số 10:", f"{(so_cau_dung / len(st.session_state.on_tap_10)) * 10:.1f} điểm")
    
    if st.button("🔄 Làm đề mới (Bốc 10 câu khác)"):
        del st.session_state.on_tap_10
        del st.session_state.on_tap_opts
        st.rerun()

# --- 5. DÀNH CHO GIÁO VIÊN: XUẤT FILE IN (ĐỊNH DẠNG HTML) ---
st.markdown("---")
st.subheader("🖨️ Dành cho Giáo viên: Xuất đề để in")

# Tạo nội dung file HTML có nhúng sẵn thư viện dịch Toán học (MathJax)
# Tạo nội dung file HTML có nhúng cấu hình MathJax nhận diện dấu $
html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Đề Ôn Tập Toán</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script>
    MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: 'Times New Roman', serif; font-size: 17px; padding: 30px; line-height: 1.5; max-width: 800px; margin: auto; }
        .cau-hoi { margin-top: 20px; font-weight: bold; }
        .dap-an { margin-left: 20px; margin-bottom: 5px; }
    </style>
</head>
<body>
    <h2 style="text-align: center;">ĐỀ ÔN TẬP TOÁN (10 CÂU NGẪU NHIÊN)</h2>
    <hr>
"""

for i, q in enumerate(st.session_state.on_tap_10):
    html_content += f"<div class='cau-hoi'>Câu {i+1}: {q['CauHoi']}</div>\n"
    opts = st.session_state.on_tap_opts[i]
    html_content += f"<div class='dap-an'>{opts[0]}</div>\n"
    html_content += f"<div class='dap-an'>{opts[1]}</div>\n"
    html_content += f"<div class='dap-an'>{opts[2]}</div>\n"
    html_content += f"<div class='dap-an'>{opts[3]}</div>\n"

html_content += """
</body>
</html>
"""

# Nút tải file HTML về máy
st.download_button(
    label="📥 Tải Bản In (Tự động dịch công thức Toán)",
    data=html_content,
    file_name="De_On_Tap_In.html",
    mime="text/html"
)

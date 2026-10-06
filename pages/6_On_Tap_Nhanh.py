import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Ôn Tập Nhanh", page_icon="⚡")
st.title("⚡ Ôn Tập Nhanh: 10 Câu Trắc Nghiệm")

# --- 1. DÙNG CHUNG LINK NGÂN HÀNG ĐỀ CỦA ANH ---
url_csv = "DÁN_LINK_CSV_CỦA_ANH_VÀO_ĐÂY"

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
    st.error("⚠️ Lỗi tải dữ liệu ngân hàng đề.")
    st.stop()

# --- 2. BỐC NGẪU NHIÊN 10 CÂU ---
if 'on_tap_10' not in st.session_state:
    p1_all = df[df['Phan'] == '1'].to_dict('records')
    
    # Lấy 10 câu (nếu ngân hàng đề có ít hơn 10 câu thì lấy tất cả)
    so_cau = min(10, len(p1_all))
    p1_random = random.sample(p1_all, so_cau)
    
    # Trộn thứ tự đáp án A, B, C, D
    p1_opts = {}
    for i, q in enumerate(p1_random):
        opts = [str(q['A']), str(q['B']), str(q['C']), str(q['D'])]
        random.shuffle(opts)
        p1_opts[i] = opts
        
    st.session_state.on_tap_10 = p1_random
    st.session_state.on_tap_opts = p1_opts

# --- 3. GIAO DIỆN LÀM BÀI ---
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
        if str(luu_bai.get(i)).strip() == str(q['DapAn']).strip():
            so_cau_dung += 1
            
    st.success(f"🎉 Em làm đúng **{so_cau_dung} / {len(st.session_state.on_tap_10)}** câu!")
    st.metric("Điểm hệ số 10:", f"{(so_cau_dung / len(st.session_state.on_tap_10)) * 10:.1f} điểm")
    
    # Nút bấm để bốc 10 câu mới
    if st.button("🔄 Làm đề mới (Bốc 10 câu khác)"):
        del st.session_state.on_tap_10
        del st.session_state.on_tap_opts
        st.rerun()

import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Đề Thi Toán 2025", page_icon="📝")
st.title("📝 Đề Kiểm Tra (Cấu trúc 2025)")

# --- 1. LINK FILE EXCEL (CSV) NGÂN HÀNG ĐỀ ---
url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgL0N3nFv1hy9T4BI5lhWl9Q7HOzuk09n6PDGlmeFYCeJcF0pQnX-s5hSsgWBj2h-5Jl6FpYoa3bPF/pub?output=csv"

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
    st.error("⚠️ Không thể tải dữ liệu từ ngân hàng đề. Vui lòng kiểm tra lại link CSV.")
    st.stop()

# --- 2. TỰ ĐỘNG TRỘN ĐỀ RIÊNG CHO TỪNG HỌC SINH ---
if 'de_da_tron' not in st.session_state:
    p1 = df[df['Phan'] == '1'].to_dict('records')
    p2 = df[df['Phan'] == '2'].to_dict('records')
    p3 = df[df['Phan'] == '3'].to_dict('records')

    # Trộn thứ tự câu hỏi ở cả 3 phần
    random.shuffle(p1)
    random.shuffle(p2)
    random.shuffle(p3)

    # Trộn thứ tự đáp án A, B, C, D cho riêng Phần 1
    p1_options = {}
    for i, q in enumerate(p1):
        opts = [str(q['A']), str(q['B']), str(q['C']), str(q['D'])]
        random.shuffle(opts)
        p1_options[i] = opts

    # Lưu cấu trúc đề đã trộn vào phiên làm việc của máy đó
    st.session_state.phan1 = p1
    st.session_state.phan2 = p2
    st.session_state.phan3 = p3
    st.session_state.p1_options = p1_options
    st.session_state.de_da_tron = True


# --- 3. GIAO DIỆN LÀM BÀI ---
st.info("📌 Học sinh điền thông tin và bấm Enter để nhận đề thi.")
col1, col2 = st.columns(2)
ho_ten = col1.text_input("Họ và Tên:")
lop = col2.text_input("Lớp:")

if ho_ten and lop:
    with st.form("exam_form"):
        luu_bai = {"p1": {}, "p2": {}, "p3": {}}

        # Giao diện Phần I
        if len(st.session_state.phan1) > 0:
            st.header("PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn")
            for i, q in enumerate(st.session_state.phan1):
                options = st.session_state.p1_options[i] # Lấy danh sách đáp án đã bị trộn
                luu_bai["p1"][i] = st.radio(f"**Câu {i+1}:** {q['CauHoi']}", options, index=None, key=f"p1_{i}")
            st.divider()

        # Giao diện Phần II
        if len(st.session_state.phan2) > 0:
            st.header("PHẦN II. Câu trắc nghiệm đúng sai")
            for i, q in enumerate(st.session_state.phan2):
                st.markdown(f"**Câu {i+1}:** {q['CauHoi']}")
                y_list = [('a', q['A']), ('b', q['B']), ('c', q['C']), ('d', q['D'])]
                for idx, (ky_hieu, noi_dung) in enumerate(y_list):
                    if str(noi_dung).strip():
                        c1, c2 = st.columns([4, 1])
                        with c1: st.write(f"**{ky_hieu})** {noi_dung}")
                        with c2: luu_bai["p2"][f"{i}_{ky_hieu}"] = st.radio("Chọn:", ["Đúng", "Sai"], key=f"p2_{i}_{ky_hieu}", index=None, horizontal=True, label_visibility="collapsed")
                st.markdown("---")

        # Giao diện Phần III
        if len(st.session_state.phan3) > 0:
            st.header("PHẦN III. Câu trắc nghiệm trả lời ngắn")
            for i, q in enumerate(st.session_state.phan3):
                luu_bai["p3"][i] = st.text_input(f"**Câu {i+1}:** {q['CauHoi']}", placeholder="Nhập đáp án...", key=f"p3_{i}")

        submitted = st.form_submit_button("✅ Nộp bài chấm điểm")

    # --- 4. LOGIC CHẤM ĐIỂM ---
    if submitted:
        diem = 0
        
        # Chấm Phần I (0.25 điểm/câu)
        for i, q in enumerate(st.session_state.phan1):
            if str(luu_bai["p1"].get(i)).strip() == str(q['DapAn']).strip(): diem += 0.25

        # Chấm Phần II (0.1 điểm/ý, 0.5 điểm/3 ý, 1.0 điểm/4 ý)
        for i, q in enumerate(st.session_state.phan2):
            dap_an_dung = [x.strip() for x in str(q['DapAn']).split(",")]
            y_dung = 0
            for idx, ky_hieu in enumerate(['a', 'b', 'c', 'd']):
                if idx < len(dap_an_dung) and luu_bai["p2"].get(f"{i}_{ky_hieu}") == dap_an_dung[idx]:
                    y_dung += 1
            if y_dung == 1: diem += 0.1
            elif y_dung == 2: diem += 0.25
            elif y_dung == 3: diem += 0.5
            elif y_dung == 4: diem += 1.0

        # Chấm Phần III (0.5 điểm/câu)
        for i, q in enumerate(st.session_state.phan3):
            if str(luu_bai["p3"].get(i)).strip() == str(q['DapAn']).strip(): diem += 0.5

        st.success(f"✅ Ghi nhận bài làm của: **{ho_ten} - {lop}**")
        st.metric("Điểm số tổng cộng:", f"{diem:.2f}")
        st.balloons()

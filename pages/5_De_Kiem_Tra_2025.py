import streamlit as st
import pandas as pd

st.set_page_config(page_title="Đề Thi Toán 2025", page_icon="📝")
st.title("📝 Đề Kiểm Tra (Cấu trúc 2025)")

# --- 1. LINK FILE EXCEL (CSV) NGÂN HÀNG ĐỀ ---
url_csv = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTDgqx6QUv8gfyrR2sXlwEH5qajv0HRiopD8D0qO_G6clTYqbxz01pbnPTrCn0LP_cdQ9rRN0FqOQjr/pub?output=csv"

@st.cache_data(ttl=60) # Cập nhật đề sau mỗi 60 giây
def load_data(url):
    try:
        df = pd.read_csv(url)
        df = df.fillna("") # Biến các ô trống thành chuỗi rỗng để không bị lỗi
        return df
    except Exception as e:
        return None

df = load_data(url_csv)

if df is None:
    st.error("⚠️ Không thể tải dữ liệu từ ngân hàng đề. Vui lòng kiểm tra lại link CSV.")
    st.stop()

# Phân loại dữ liệu theo 3 phần
phan1 = df[df['Phan'] == 1].to_dict('records')
phan2 = df[df['Phan'] == 2].to_dict('records')
phan3 = df[df['Phan'] == 3].to_dict('records')

# --- 2. GIAO DIỆN LÀM BÀI ---
st.info("📌 Học sinh điền thông tin để nhận đề thi.")
col1, col2 = st.columns(2)
ho_ten = col1.text_input("Họ và Tên:")
lop = col2.text_input("Lớp:")

if ho_ten and lop:
    with st.form("exam_form"):
        luu_bai = {"p1": {}, "p2": {}, "p3": {}}

        # Giao diện Phần I
        if len(phan1) > 0:
            st.header("PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn")
            for i, q in enumerate(phan1):
                options = [q['A'], q['B'], q['C'], q['D']]
                luu_bai["p1"][i] = st.radio(f"**Câu {i+1}:** {q['CauHoi']}", options, index=None, key=f"p1_{i}")
            st.divider()

        # Giao diện Phần II
        if len(phan2) > 0:
            st.header("PHẦN II. Câu trắc nghiệm đúng sai")
            for i, q in enumerate(phan2):
                st.markdown(f"**Câu {i+1}:** {q['CauHoi']}")
                # Tách chuỗi đáp án "Đúng, Sai, Sai, Đúng" thành list
                dap_an_dung = [x.strip() for x in str(q['DapAn']).split(",")]
                
                # Render 4 ý
                y_list = [('a', q['A']), ('b', q['B']), ('c', q['C']), ('d', q['D'])]
                for idx, (ky_hieu, noi_dung) in enumerate(y_list):
                    if noi_dung: # Chỉ hiện nếu có nội dung
                        c1, c2 = st.columns([4, 1])
                        with c1: 
                            st.write(f"**{ky_hieu})** {noi_dung}")
                        with c2: 
                            luu_bai["p2"][f"{i}_{ky_hieu}"] = st.radio(
                                "Chọn:", ["Đúng", "Sai"], 
                                key=f"p2_{i}_{ky_hieu}", 
                                index=None, 
                                horizontal=True, 
                                label_visibility="collapsed"
                            )
                st.markdown("---")

        # Giao diện Phần III
        if len(phan3) > 0:
            st.header("PHẦN III. Câu trắc nghiệm trả lời ngắn")
            for i, q in enumerate(phan3):
                luu_bai["p3"][i] = st.text_input(f"**Câu {i+1}:** {q['CauHoi']}", placeholder="Nhập đáp án (chỉ ghi số)...", key=f"p3_{i}")

        submitted = st.form_submit_button("✅ Nộp bài chấm điểm")

    # --- 3. LÔ-GIC CHẤM ĐIỂM ---
    if submitted:
        diem = 0
        
        # Chấm Phần I (Giả sử 0.25 điểm/câu)
        for i, q in enumerate(phan1):
            if luu_bai["p1"].get(i) == q['DapAn']: 
                diem += 0.25

        # Chấm Phần II (0.1 điểm/ý, 0.5 điểm/câu đúng cả 4 ý - theo quy chế Bộ)
        for i, q in enumerate(phan2):
            dap_an_dung = [x.strip() for x in str(q['DapAn']).split(",")]
            y_dung = 0
            ky_hieu_list = ['a', 'b', 'c', 'd']
            for idx, ky_hieu in enumerate(ky_hieu_list):
                # Kiểm tra tránh lỗi out of index nếu nhập thiếu đáp án trong Excel
                if idx < len(dap_an_dung) and luu_bai["p2"].get(f"{i}_{ky_hieu}") == dap_an_dung[idx]:
                    y_dung += 1
            
            # Thang điểm chuẩn Phần II
            if y_dung == 1: diem += 0.1
            elif y_dung == 2: diem += 0.25
            elif y_dung == 3: diem += 0.5
            elif y_dung == 4: diem += 1.0

        # Chấm Phần III (0.5 điểm/câu)
        for i, q in enumerate(phan3):
            da_hs = str(luu_bai["p3"].get(i)).strip()
            da_chuan = str(q['DapAn']).strip()
            # Xóa ".0" nếu Excel tự động thêm vào số nguyên
            if da_chuan.endswith(".0"): da_chuan = da_chuan[:-2] 
            
            if da_hs == da_chuan: 
                diem += 0.5

        st.success(f"✅ Ghi nhận bài làm của: **{ho_ten} - {lop}**")
        st.metric("Điểm số tổng cộng:", f"{diem:.2f}")
        st.balloons()

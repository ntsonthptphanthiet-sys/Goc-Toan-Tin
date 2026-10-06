import streamlit as st

st.set_page_config(page_title="Đề Thi Toán 2025", page_icon="📝")
st.title("📝 Đề Kiểm Tra (Cấu trúc 2025)")
st.caption("Chuyên đề: Mệnh đề - Tập hợp")

# --- 1. DỮ LIỆU ĐỀ THI MẪU (Anh Sơn dán thêm câu hỏi vào đây) ---
phan1 = [
    {
        "cau": "Mệnh đề nào sau đây là mệnh đề đúng?", 
        "dap_an": ["A. $\exists x\in\mathbb{R}:x^{2}\le x$", "B. $\exists x\in\mathbb{N}:x^{2}+8x+7=0$", "C. $\forall x\in\mathbb{R}:|x|>0$", "D. $\exists x\in\mathbb{R}:-x^{2}>0$"], 
        "dung": "A. $\exists x\in\mathbb{R}:x^{2}\le x$"
    }
]

phan2 = [
    {
        "cau": "Cho $P(n)=n^{2}-6n+10$ với $n$ là số tự nhiên.",
        "y_a": "a) $P(1)$ chia hết cho 3.", "da_a": "Sai",
        "y_b": "b) $P(2)$ là số lẻ.", "da_b": "Sai",
        "y_c": "c) $P(2n)>P(n)-1$ với $n=1$.", "da_c": "Sai",
        "y_d": "d) Tồn tại số tự nhiên $n$ thỏa mãn $\\frac{2P(n)-1}{n-3}$ là số nguyên.", "da_d": "Đúng"
    }
]

phan3 = [
    {
        "cau": "Cho hai tập hợp $A=(0;5]$ và $B=\{-2;1;3;6\}$. Số phần tử của $(A\cup B)\cap\mathbb{Z}$ bằng bao nhiêu?", 
        "dung": "6"
    }
]

# --- 2. GIAO DIỆN LÀM BÀI ---
st.info("📌 Học sinh điền thông tin để bắt đầu làm bài.")
col1, col2 = st.columns(2)
ho_ten = col1.text_input("Họ và Tên:")
lop = col2.text_input("Lớp:")

if ho_ten and lop:
    with st.form("exam_form"):
        luu_bai = {"p1": {}, "p2": {}, "p3": {}}

        # Giao diện Phần I
        st.header("PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn")
        st.markdown("*(Thí sinh chọn 1 đáp án đúng nhất)*")
        for i, q in enumerate(phan1):
            luu_bai["p1"][i] = st.radio(f"**Câu {i+1}:** {q['cau']}", q['dap_an'], index=None)
        
        st.divider()

        # Giao diện Phần II
        st.header("PHẦN II. Câu trắc nghiệm đúng sai")
        st.markdown("*(Trong mỗi ý a, b, c, d, thí sinh chọn Đúng hoặc Sai)*")
        for i, q in enumerate(phan2):
            st.markdown(f"**Câu {i+1}:** {q['cau']}")
            # Tạo 4 dòng cho 4 ý, mỗi dòng chia 2 cột (Cột đề bài : Cột nút chọn)
            for y, da_key in [('y_a', 'da_a'), ('y_b', 'da_b'), ('y_c', 'da_c'), ('y_d', 'da_d')]:
                c1, c2 = st.columns([4, 1])
                with c1: 
                    st.write(q[y])
                with c2: 
                    # label_visibility="collapsed" giúp giấu chữ tiêu đề của nút chọn cho gọn
                    luu_bai["p2"][f"{i}_{y}"] = st.radio("Chọn:", ["Đúng", "Sai"], key=f"p2_{i}_{y}", index=None, horizontal=True, label_visibility="collapsed")
            st.markdown("---")

        # Giao diện Phần III
        st.header("PHẦN III. Câu trắc nghiệm trả lời ngắn")
        st.markdown("*(Thí sinh điền đáp án dạng số vào ô trống)*")
        for i, q in enumerate(phan3):
            luu_bai["p3"][i] = st.text_input(f"**Câu {i+1}:** {q['cau']}", placeholder="Nhập đáp án (chỉ ghi số)...")

        submitted = st.form_submit_button("✅ Nộp bài chấm điểm")

    # --- 3. LOGIC CHẤM ĐIỂM ---
    if submitted:
        diem = 0
        
        # Chấm Phần I (Giả sử 0.25 điểm/câu)
        for i, q in enumerate(phan1):
            if luu_bai["p1"][i] == q['dung']: 
                diem += 0.25

        # Chấm Phần II (Giả sử 0.1 điểm/ý đúng, đúng cả câu 4 ý được thêm điểm)
        for i, q in enumerate(phan2):
            if luu_bai["p2"][f"{i}_y_a"] == q['da_a']: diem += 0.1
            if luu_bai["p2"][f"{i}_y_b"] == q['da_b']: diem += 0.1
            if luu_bai["p2"][f"{i}_y_c"] == q['da_c']: diem += 0.1
            if luu_bai["p2"][f"{i}_y_d"] == q['da_d']: diem += 0.1

        # Chấm Phần III (Giả sử 0.5 điểm/câu)
        for i, q in enumerate(phan3):
            if luu_bai["p3"][i].strip() == q['dung']: 
                diem += 0.5

        st.success(f"✅ Ghi nhận bài làm của: **{ho_ten} - {lop}**")
        st.metric("Điểm số tạm tính:", f"{diem:.2f}")
        st.balloons()

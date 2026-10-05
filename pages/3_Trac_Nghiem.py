import streamlit as st
import random
import requests

st.set_page_config(page_title="Ôn tập Toán", page_icon="📝")
st.title("📝 Bài Tập Ôn Tập (Trộn đề tự động)")

# 1. TẠO NGÂN HÀNG CÂU HỎI
if 'ngan_hang' not in st.session_state:
    danh_sach_cau_hoi = [
        {"id": 1, "cau": "Đạo hàm của hàm số $y = x^3 - 3x^2 + 2$ là:", "dap_an": ["$3x^2 - 6x$", "$3x^2 - 3x$", "$x^2 - 6x$", "$3x^2 + 6x$"], "dung": "$3x^2 - 6x$"},
        {"id": 2, "cau": "Tọa độ đỉnh của parabol $y = x^2 - 4x + 3$ là:", "dap_an": ["$I(2; -1)$", "$I(2; 1)$", "$I(-2; 15)$", "$I(-2; -1)$"], "dung": "$I(2; -1)$"},
        {"id": 3, "cau": "Tập xác định của hàm số $y = \log_2(x - 1)$ là:", "dap_an": ["$(1; +\infty)$", "$[1; +\infty)$", "$(0; +\infty)$", "$\mathbb{R} \setminus \{1\}$"], "dung": "$(1; +\infty)$"},
        {"id": 4, "cau": "Nghiệm của phương trình $2^{x+1} = 8$ là:", "dap_an": ["$x = 2$", "$x = 3$", "$x = 1$", "$x = 4$"], "dung": "$x = 2$"}
    ]
    
    # Trộn thứ tự câu hỏi
    random.shuffle(danh_sach_cau_hoi)
    
    # Trộn thứ tự đáp án bên trong mỗi câu
    for q in danh_sach_cau_hoi:
        random.shuffle(q["dap_an"])
        
    # Lưu vào bộ nhớ tạm của học sinh đó
    st.session_state.ngan_hang = danh_sach_cau_hoi

# 2. XÁC NHẬN DANH TÍNH HỌC SINH
st.info("📌 Các em hãy nhập thông tin để nhận đề thi của riêng mình.")
col1, col2 = st.columns(2)
ho_ten = col1.text_input("Nhập Họ và Tên:")
lop = col2.text_input("Nhập Lớp (VD: 11A1):")

# Chỉ khi học sinh nhập đủ tên và lớp thì mới hiện đề
if ho_ten and lop:
    st.success(f"👋 Chào **{ho_ten}** - Lớp **{lop}**. Đề thi của em đã sẵn sàng!")
    
    # Bắt đầu form làm bài
    with st.form("quiz_form"):
        luu_bai_lam = {} # Biến lưu các đáp án học sinh chọn
        
        # Duyệt qua các câu hỏi đã được trộn
        for i, q in enumerate(st.session_state.ngan_hang):
            st.markdown(f"**Câu {i+1}:** {q['cau']}")
            # Hiển thị các đáp án
            chon = st.radio("Chọn đáp án:", q['dap_an'], index=None, key=f"cau_{q['id']}")
            luu_bai_lam[q['id']] = chon
            st.divider()
            
        submitted = st.form_submit_button("✅ Nộp bài chấm điểm")
        
    # 3. XỬ LÝ CHẤM ĐIỂM SAU KHI NỘP
    if submitted:
        diem = 0
        cau_dung = 0
        so_cau = len(st.session_state.ngan_hang)
        
        # Đếm số câu đúng
        for q in st.session_state.ngan_hang:
            if luu_bai_lam[q['id']] == q['dung']:
                diem += 10 / so_cau  # Chấm thang điểm 10
                cau_dung += 1
                
        # Hiển thị điểm trên màn hình
        st.metric(label="Điểm của em", value=f"{diem:.1f} điểm", delta=f"Đúng {cau_dung}/{so_cau} câu")
        
        if diem >= 8:
            st.balloons()
            
        # --- ĐOẠN GỬI ĐIỂM VỀ GOOGLE SHEETS ---
        # Link formResponse chuẩn
        url_form = "https://docs.google.com/forms/d/e/1FAIpQLSfHG-J5lyLzLmG-5HSdJdee8khJf7Ilg5wR83j2vz6W502AtQ/formResponse"
        
        # Đóng gói dữ liệu với 3 mã Entry ID đã lấy
        form_data = {
            "entry.1995048682": ho_ten,                # Mã ô Họ và Tên
            "entry.1508035046": lop,                   # Mã ô Lớp
            "entry.678203493": str(round(diem, 1))     # Mã ô Điểm
        }
        
        try:
            # Gửi dữ liệu đi
            response = requests.post(url_form, data=form_data)
            if response.status_code == 200:
                st.success(f"✅ Đã ghi nhận điểm của **{ho_ten}** ({lop}) vào bảng điểm của thầy Sơn thành công!")
            else:
                st.warning("⚠ Đã chấm điểm, nhưng chưa lưu được vào hệ thống.")
        except Exception as e:
            st.error("⚠️ Lỗi mạng: Không thể gửi điểm. Em hãy chụp màn hình điểm số báo cho thầy nhé.")

else:
    st.warning("⚠️ Đề thi đang bị khóa. Hãy nhập đủ Họ tên và Lớp để mở đề.")

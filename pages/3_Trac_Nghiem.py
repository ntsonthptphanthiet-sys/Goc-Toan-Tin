# 3. XỬ LÝ CHẤM ĐIỂM SAU KHI NỘP
    if submitted:
        diem = 0
        cau_dung = 0
        so_cau = len(st.session_state.ngan_hang)
        
        for q in st.session_state.ngan_hang:
            if luu_bai_lam[q['id']] == q['dung']:
                diem += 10 / so_cau  # Chấm thang điểm 10
                cau_dung += 1
                
        st.metric(label="Điểm của em", value=f"{diem:.1f} điểm", delta=f"Đúng {cau_dung}/{so_cau} câu")
        
        if diem >= 8:
            st.balloons()
            
        # --- BẮT ĐẦU ĐOẠN GỬI ĐIỂM VỀ GOOGLE SHEETS CỦA THẦY SƠN ---
        # Link formResponse chuẩn
        url_form = "https://docs.google.com/forms/d/e/1FAIpQLSfHG-J5lyLzLmG-5HSdJdee8khJf7Ilg5wR83j2vz6W502AtQ/formResponse"
        
        # Đóng gói dữ liệu với 3 mã Entry ID anh vừa lấy được
        form_data = {
            "entry.1995048682": ho_ten,                # Mã ô Họ và Tên
            "entry.1508035046": lop,                   # Mã ô Lớp
            "entry.678203493": str(round(diem, 1))     # Mã ô Điểm (Làm tròn 1 chữ số thập phân)
        }
        
        try:
            import requests # Đảm bảo đã import thư viện
            # Gửi dữ liệu đi
            response = requests.post(url_form, data=form_data)
            if response.status_code == 200:
                st.success(f"✅ Đã ghi nhận điểm của **{ho_ten}** ({lop}) vào bảng điểm của thầy Sơn thành công!")
            else:
                st.warning("⚠️️ Đã chấm điểm, nhưng chưa lưu được vào hệ thống.")
        except Exception as e:
            st.error("⚠️ Lỗi mạng: Không thể gửi điểm. Em hãy chụp màn hình điểm số báo cho thầy nhé.")

st.markdown("---")
st.subheader("🖨️ Dành cho Giáo viên: Xuất đề để in")

# Tạo định dạng nội dung Đề thi để tải về
noi_dung_de = "ĐỀ ÔN TẬP TOÁN (10 CÂU NGẪU NHIÊN)\n"
noi_dung_de += "-" * 40 + "\n\n"

for i, q in enumerate(st.session_state.on_tap_10):
    noi_dung_de += f"Câu {i+1}: {q['CauHoi']}\n"
    opts = st.session_state.on_tap_opts[i]
    noi_dung_de += f"A. {opts[0]}\nB. {opts[1]}\nC. {opts[2]}\nD. {opts[3]}\n\n"

# Thêm nút bấm tải file về máy
st.download_button(
    label="📥 Tải Đề này về máy (File Text)",
    data=noi_dung_de,
    file_name="De_On_Tap_Ngau_Nhien.txt",
    mime="text/plain"
)

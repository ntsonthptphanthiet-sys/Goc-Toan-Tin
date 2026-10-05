import streamlit as st

st.set_page_config(page_title="Luyện tập Trắc nghiệm", page_icon="📝")

st.title("📝 Luyện tập Trắc nghiệm Củng cố")
st.info("Học sinh chọn đáp án đúng cho từng câu hỏi và bấm nút Nộp bài để xem điểm.")

# Dùng form để gom nhóm các câu hỏi, tránh việc web tự tải lại khi đang chọn dở đáp án
with st.form("quiz_form"):
    st.markdown("### **Câu 1:**")
    st.markdown("Đạo hàm của hàm số $y = x^3 - 3x^2 + 2$ là:")
    # index=None giúp bỏ chọn mặc định, yêu cầu học sinh phải tự click
    q1 = st.radio(
        "Chọn 1 đáp án:",
        options=["A. $y' = 3x^2 - 6x$", "B. $y' = 3x^2 - 3x$", "C. $y' = x^2 - 6x$", "D. $y' = 3x^2 + 6x$"],
        index=None,
        key="cau1"
    )

    st.divider() # Đường kẻ ngang phân cách

    st.markdown("### **Câu 2:**")
    st.markdown("Tọa độ đỉnh của parabol $(P): y = x^2 - 4x + 3$ là:")
    q2 = st.radio(
        "Chọn 1 đáp án:",
        options=["A. $I(2; 1)$", "B. $I(-2; 15)$", "C. $I(2; -1)$", "D. $I(-2; -1)$"],
        index=None,
        key="cau2"
    )

    st.divider()
    
    # Nút nộp bài
    submitted = st.form_submit_button("✅ Nộp bài chấm điểm")

# Xử lý logic chấm điểm sau khi học sinh bấm nộp
if submitted:
    diem = 0
    # Chấm câu 1
    if q1 == "A. $y' = 3x^2 - 6x$":
        diem += 1
        st.success("Câu 1: Chính xác! 🎉")
    else:
        st.error("Câu 1: Sai. Đáp án đúng là **A**.")

    # Chấm câu 2
    if q2 == "C. $I(2; -1)$":
        diem += 1
        st.success("Câu 2: Chính xác! 🎉")
    else:
        st.error(f"Câu 2: Sai. Bạn đã chọn {q2}. Đáp án đúng là **C. $I(2; -1)$**.")

    # Hiển thị tổng điểm
    st.metric(label="Tổng điểm của bạn", value=f"{diem}/2")
    
    if diem == 2:
        st.balloons() # Hiệu ứng bóng bay chúc mừng nếu đúng hết

import streamlit as st

# Tạo thanh trượt k từ -3.0 đến 3.0, bước nhảy 0.1
k = st.slider(
    label="Chọn hệ số k:", 
    min_value=-3.0, 
    max_value=3.0, 
    value=1.0,  # Giá trị mặc định ban đầu
    step=0.1
)

# Lệnh này dùng để in thử giá trị k ra màn hình web
st.write(f"Giá trị k đang chọn là: {k}")

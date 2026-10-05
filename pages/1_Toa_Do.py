import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Cấu hình trang web
st.set_page_config(page_title="Tool Tọa Độ Hóa", layout="centered")

# CSS tùy chỉnh để làm giao diện giống app (Dark mode)
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: white; }
    div[data-testid="stMetricValue"] { font-size: 1.2rem; color: #4facfe; }
    .stAlert { background-color: #1e293b; color: #e2e8f0; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("### 🟦 BƯỚC 1: Gắn hệ trục cho khéo")

# 1. Thiết lập hàm số toán học
def parabola(x):
    return 0.5 * x**2 - 2 * x + 3.5

def line_bc(x):
    # Đường thẳng qua B(0, 3.5) và C(3, 2)
    return -0.5 * x + 3.5

# 2. Tạo dữ liệu điểm để vẽ
x_vals = np.linspace(0, 3, 100)
y_para = parabola(x_vals)
y_line = line_bc(x_vals)

# 3. Vẽ đồ thị với Plotly
fig = go.Figure()

# Vẽ vùng không gian Hồ sen (fill màu giữa đường thẳng và parabol)
fig.add_trace(go.Scatter(
    x=x_vals, y=y_line, mode='lines', line=dict(color='rgba(0,0,0,0)'), showlegend=False, hoverinfo='skip'
))
fig.add_trace(go.Scatter(
    x=x_vals, y=y_para, mode='lines', 
    fill='tonexty', fillcolor='rgba(138, 43, 226, 0.3)', # Màu tím nhạt
    line=dict(color='#00ffff', width=3), # Đường viền Parabol màu Cyan
    name='Parabol'
))

# Vẽ đoạn thẳng BC
fig.add_trace(go.Scatter(
    x=[0, 3], y=[3.5, 2], mode='lines',
    line=dict(color='#a78bfa', width=2), name='Mép hồ'
))

# Vẽ các điểm A, B, I, C, D
points_x = [0, 2, 3, 3, 0]
points_y = [3.5, 1.5, 2, 0, 0]
labels = ['<b>B(0; 3.5)</b>', '<b>I(2; 1.5)</b>', '<b>C</b>', '<b>D(3; 0)</b>', '<b>A</b>']
positions = ['top right', 'bottom center', 'top right', 'top right', 'bottom left']
colors = ['#f59e0b', '#c084fc', 'white', '#38bdf8', 'gray']

fig.add_trace(go.Scatter(
    x=points_x, y=points_y, mode='markers+text',
    marker=dict(size=12, color=colors), text=labels,
    textposition=positions, textfont=dict(color=colors, size=14), showlegend=False
))

# 4. Tùy chỉnh giao diện trục tọa độ
fig.update_layout(
    template="plotly_dark",
    plot_bgcolor='#0b1120', paper_bgcolor='#0b1120',
    xaxis=dict(range=[-0.5, 3.5], dtick=1, showgrid=True, gridcolor='#1e293b', zerolinecolor='gray', title="x"),
    yaxis=dict(range=[-0.5, 4], dtick=1, showgrid=True, gridcolor='#1e293b', zerolinecolor='gray', title="y"),
    margin=dict(l=20, r=20, t=30, b=20), height=450
)

# Hiển thị biểu đồ lên web
st.plotly_chart(fig, use_container_width=True)

# 5. Giao diện Text bên dưới đồ thị (Giống trong ảnh)
st.info("""
🔹 Gốc tọa độ đặt ngay góc vuông của vườn: cạnh đáy là $Ox$, cạnh đứng là $Oy$.  
🔹 Mỗi đơn vị trên trục ứng với **10 m** - số sẽ đẹp hẳn.
""")

col1, col2, col3 = st.columns(3)
col1.metric("Cạnh đứng", "B(0 ; 3.5)")
col2.metric("Đỉnh parabol", "I(2 ; 1.5)")
col3.metric("Cạnh đáy", "D(3 ; 0)")

st.success("20 m và 15 m thành **2** và **1.5** - dữ kiện đã hoá toạ độ.")

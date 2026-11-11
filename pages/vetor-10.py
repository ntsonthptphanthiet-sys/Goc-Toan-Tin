import streamlit as st

k = st.slider("Chọn giá trị k", min_value=-3.0, max_value=3.0, step=0.1)
A = (0, 0)
B = (3, 0)
u = Vector(A, B)
M = A + k * u
v = Vector(A, M)
SetColor(v, "Red")
SetLineThickness(v, 7)

import streamlit as st

# Cấu hình trang
st.set_page_config(page_title="Tính Lãi Gửi Tiết Kiệm", page_icon="💰", layout="centered")

st.title("💰 Ứng dụng Tính Lãi Tiết Kiệm")
st.markdown("Nhập các thông tin bên dưới để tính toán số tiền lãi nhận được.")

# Tạo form nhập liệu
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input("Số tiền gửi (VNĐ)", min_value=0.0, value=100000000.0, step=1000000.0, format="%f")
    ky_han = st.number_input("Kỳ hạn gửi (Tháng)", min_value=1, value=12, step=1)

with col2:
    lai_suat = st.number_input("Lãi suất (%/năm)", min_value=0.0, value=6.0, step=0.1, format="%f")
    hinh_thuc = st.selectbox("Hình thức nhận lãi", ["Cuối kỳ", "Hàng tháng", "Hàng quý"])

# Hàm định dạng tiền tệ
def format_vnd(amount):
    return f"{amount:,.0f} VNĐ"

if st.button("Tính toán", type="primary"):
    # Công thức chung tính tổng lãi: Gốc * Lãi suất/năm * (Số tháng/12)
    tong_tien_lai = so_tien_gui * (lai_suat / 100) * (ky_han / 12)
    
    tien_lai_dinh_ky = 0
    chu_ky_nhan = ""

    # Xử lý logic chia tiền lãi theo hình thức nhận
    if hinh_thuc == "Cuối kỳ":
        tien_lai_dinh_ky = tong_tien_lai
        chu_ky_nhan = "cuối kỳ"
        
    elif hinh_thuc == "Hàng tháng":
        tien_lai_dinh_ky = tong_tien_lai / ky_han
        chu_ky_nhan = "mỗi tháng"
        
    elif hinh_thuc == "Hàng quý":
        so_quy = ky_han / 3
        if so_quy < 1:
            st.warning("⚠️ Kỳ hạn gửi nhỏ hơn 1 quý (3 tháng). Hình thức nhận lãi hàng quý không hợp lệ.")
        else:
            tien_lai_dinh_ky = tong_tien_lai / so_quy
            chu_ky_nhan = "mỗi quý"

    tong_thu_nhap = so_tien_gui + tong_tien_lai

    # Hiển thị bảng kết quả
    st.divider()
    st.subheader("📊 Kết quả tính toán")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Tổng tiền lãi", format_vnd(tong_tien_lai))
    res_col2.metric(f"Tiền lãi {chu_ky_nhan}", format_vnd(tien_lai_dinh_ky))
    res_col3.metric("Tổng gốc + lãi", format_vnd(tong_thu_nhap))
    
    if chu_ky_nhan and tien_lai_dinh_ky > 0:
        st.success(f"Với số tiền gốc **{format_vnd(so_tien_gui)}**, gửi trong **{ky_han} tháng** với lãi suất **{lai_suat}%/năm**, bạn sẽ nhận được tổng cộng **{format_vnd(tong_tien_lai)}** tiền lãi. Tiền lãi sẽ được thanh toán **{chu_ky_nhan}** với số tiền là **{format_vnd(tien_lai_dinh_ky)}**.")

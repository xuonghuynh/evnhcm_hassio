# Mô tả
Đây là custom component cho hệ thống nhà thông minh Home Assistant dùng để lấy dữ liệu điện tiêu thụ từ Điện lực HCM



# Cài đặt
1. Download folder tại đây: [Download](https://github.com/xuonghuynh/evnhcm_hassio/archive/refs/tags/Beta.zip) 
2. Giải nén, sau khi giải nén sẽ thấy folder `custom_components` 
3. Copy `custom_components` vào thư mục mà Home Assistant của bạn đang chạy
4. Thêm Sensor vào file `configuration.yaml` như sau:
``` yaml
sensor:
  - platform: evnhcm
    name: Phone             # Thay "Phone" bằng số điện thoại của bạn khi đăng nhập vào EVNHCM
    matkhau: Password       # Tương tự thay "Password" bằng mật khẩu của bạn
    makhach: PE00000000000  # Mã khách hàng
```
5. Restart lại Home Assistant
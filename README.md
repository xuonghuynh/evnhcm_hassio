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

# Thêm chart vào lovelace
1. Để thêm chart vào lovelace và theo dõi điện theo từng ngày, các bạn phải cài `apexcharts-card`. Hướng dẫn cài đặt apex-chart ở đây [apexcharts-card](https://github.com/RomRider/apexcharts-card). Note: nên cài qua HACS cho dể
2. Thêm code này vào lovelace 
``` yaml
type: custom:apexcharts-card
graph_span: 10d         # Số ngày bạn muốn hiển thị trên chart. Ví dụ: 3d, 5d, 1w, 1m
header:
  show: true
  title: Điện Tiêu Thụ
series:
  - entity: sensor.evnhcm
    type: column
    data_generator: |
        let array = []
        entity.attributes.ngay_chart.map((date, index) => {
            const dateString = moment(date, "DD/MM/YYYY").toDate();
            const sanluong = parseFloat(entity.attributes.san_luong_chart[index])
            const ngay = new Date(dateString).getTime()
            array.push([ngay, sanluong]);
        })
        return array;
```
![Chart](https://github.com/xuonghuynh/evnhcm_hassio/blob/main/assets/chart.png)
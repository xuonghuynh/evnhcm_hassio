import datetime
# from .app import API
import evnhcm

class Init:
    def __init__(self, name='evnhcm', matkhau='' , makhach='', numday=''):
        self._state = ''
        self._name = name
        self._matkhau = matkhau
        self._makhach = makhach
        self._numday = numday
        self._listngay = []
        self._sanluong = []
        self._attribute = {}

    @property
    def state(self):
        return self._state

    @property
    def attribute(self):
        return self._attribute

class HassioVersion(Init):
    def bill_data(self):
        today = datetime.datetime.now()
        try:  
            api = evnhcm.API(self._name , self._matkhau)
            _res_data = api.get_evn_hcm(self._makhach)
            
        except:
            print("Xảy ra lỗi ! Không lấy được dữ liệu !")
        tam_tinh = float(_res_data['sanluong_tong']) * 2834
        if  _res_data['state'] in ['error']:
          self._state = '0'
          self._attribute["error"] = "Không lấy được dữ liệu"
        else:
          self._listngay = []
          self._sanluong = []
          sanluong_tong = _res_data['sanluong_tong']
          sanluong_tong = float(sanluong_tong)
          self._state = sanluong_tong
          self._attribute["tieu_de"] = "Sản lượng điện sử dụng"
          self._attribute["thoi_diem_do"] = _res_data['thoidiemdo']
          self._attribute["san_luong_ngay"] = _res_data['sanluong_tong']
          self._attribute["san_luong_thang"] = _res_data['data_dien_su_dung']['sanluong_tong']['Tong']
          self._attribute["san_luong_tong"] = self._attribute["san_luong_thang"] * 2834
          self._attribute["tien_tam_tinh"] = str(round(tam_tinh, 2)) + ' VNĐ'
          # Hóa đơn từng tháng
          for i in _res_data['data_hoa_don']:
            self._attribute["thang_"+i['THANG']+"_"+i['NAM']] = i['TONG_TIEN'] + ' VNĐ'
            if i['TRANGTHAI'] != 0:
              self._attribute["trang_thai_thang_"+i['THANG']] = "Chưa thanh toán"
            else:
              self._attribute["thang_"+i['THANG']] = "Đã thanh toán"
          # Dùng cho chart lovelace
          for i in _res_data['data_dien_su_dung']['sanluong_tungngay']:
            self._listngay.append(i['ngayFull'])
            self._sanluong.append(i['sanluong_BT'])
          # Show chart data on state
          self._attribute["ngay_chart"] = self._listngay
          self._attribute["san_luong_chart"] = self._sanluong
          # Energy
          self._attribute["device_class"] = 'energy'
          self._attribute["state_class"] = 'measurement'
          self._attribute["unit_of_measurement"] = 'kWh'
          
          self._attribute["last_reset"] = today.strftime("%Y-%m-%dT00:00:00+00:00")

    def total_bill_data(self):
      try:  
        api = evnhcm.API(self._name , self._matkhau)
        _res_data = api.get_evn_hcm(self._makhach)
        print(_res_data)
      except:
        print("Xảy ra lỗi ! Không lấy được dữ liệu !")

      if _res_data['state'] in ['error']:
        self._state = 0
        self._attribute["alert"] = "Error"
      else:
        today = datetime.datetime.now()
        tong_tien = _res_data['data_dien_su_dung']['sanluong_tong']['Tong'] * 2834
        self._state = tong_tien
        self._attribute["tieu_de"] = "Tổng tiền điện trong tháng"
        self._attribute["state_class"] = 'total'
        self._attribute["device_class"] = 'monetary'
        self._attribute["unit_of_measurement"] = 'VND'
        self._attribute["last_reset"] = today.strftime("%Y/%m/%dT00:00:00+00:00")
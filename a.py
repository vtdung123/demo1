import serial

ser = serial.Serial('/dev/ttyUSB0',9600)
print (ser.isOpen)
while True:

    data = ser.read_until()
    print (data,type(data))
    dk=data[0:1]
    if dk ==b'\x02':
        data_cut = data[5:11]
    else:

        data_cut = data[6:12] 
    print(data_cut)
    d = data_cut.decode()
    print (d,type(d))
    kq = int(d,16)
    print (kq,type(kq))
        
  
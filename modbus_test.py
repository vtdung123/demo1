
from pymodbus.client.sync import ModbusSerialClient

client = ModbusSerialClient(method = 'rtu', baudrate= 115200, port='/dev/ttyUSB0', stopbits= 1, paraity= 'N', bytesize=8)
connection = client.connect()
print (connection)
while True:

    result =client.read_holding_registers(2,11,unit=0x01)
    print (result.registers)
    response=[0 for i in range(11)]
    for k in range(0,11):
        if result.registers[k] > 6000:
            result.registers[k] = result.registers[k] - 65535
            result.registers[k] = -result.registers[k]
            if result.registers[k] < 50 :
                result.registers[k] = 0
            response[k]=result.registers[k]
            
    print (response)

#!/usr/bin/env python
import rospy
from pymodbus.client.sync import ModbusTcpClient
from modbus_node.msg import Read_PLC
from modbus_node.msg import Write_PLC

client = ModbusTcpClient('192.168.5.24','502')

def callback(Write_PLC):
    client.write_coils(Write_PLC.Position_Output,Write_PLC.Array_Data_Output)
    client.write_registers(Write_PLC.Position_Registers,Write_PLC.Array_Data_Registers)
def PLC():
    rospy.init_node('PLC',anonymous=True)
    pub = rospy.Publisher('Read_FX_CPU', Read_PLC,queue_size=100)
    sub = rospy.Subscriber('Write_to_PLC',Write_PLC,callback)

    start_coils = rospy.get_param("~Modbus/Write_Output/Write_Output_Position",0)
    data_array_coils = rospy.get_param("~Modbus/Write_Output/Write_Output_Array_Data",[0])
    client.write_coils(start_coils,data_array_coils)
    start_registers = rospy.get_param("~Modbus/Write_Regiters/Write_Registers_Posittion",0)
    data_array_registers =  rospy.get_param("~Modbus/Write_Registers/Write_Registers_Array_Data",[])
    client.write_registers(start_registers,data_array_registers)
    start_input = rospy.get_param("~Modbus/Read_Input/Read_Input_Posittion",0)
    number_input = rospy.get_param("~Modbus/Read_Output/Read_Output_Number",100)
    start_output = rospy.get_param("~Modbus/Read_Output/Read_Output_Position",0)
    number_output = rospy.get_param("~Modbus/Read_Output/Read_Output_Number",100)
    start_read_registers = rospy.get_param("~Modbus/Read_Registers/Read_Registers_Position",0)
    number_read_registers = rospy.get_param("~Modbus/Read_Registers/Read_Registers_Number",125)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        public = Read_PLC()
        Input_PLC = client.read_discrete_inputs(start_input,number_input)
        Output_PLC = client.read_coils(start_output,number_output)
        Registers_PLC =client.read_holding_registers(start_read_registers,number_read_registers)
        Input_PLC_Pub = Input_PLC.bits
        Output_PLC_Pub = Output_PLC.bits
        Registers_PLC_Pub = Registers_PLC.registers
        public.Read_Input = Input_PLC_Pub
        public.Read_OutPut = Output_PLC_Pub
        public.Read_Registers = Registers_PLC_Pub
        pub.publish(public)
        rate.sleep()
    rospy.spin()
if __name__ == '__main__':
    try:
        PLC()
    except rospy.ROSInterruptException:
         pass

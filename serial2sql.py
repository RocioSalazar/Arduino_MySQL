import serial
from serial import SerialException
from DatabaseControl import DatabaseControl
import json
import os
import sys

class serial2sql:

    def __init__(self,param):
        self.parameters = param
        self.output = False
        self.loadParameters()

    def loadParameters(self):
        with open(self.parameters)as f:
            self.param = json.load(f)

        self.dbC = DatabaseControl(self.param)
        #self.dbC.createTable()

    def setOutput(self,outputFile):
        self.dbC.setOutPutFile(outputFile)

    def run(self):
        self.dbC.createTable()
        print("Puerto abierto y comenzando a guardar datos")
        print("Presiona Ctrl+C para detener el programa")
        try:
            ser = serial.Serial(self.param["puerto"], self.param["baudios"], timeout=1)
            ser.readline() #Line with no data
            while(True):
                line = str(ser.readline()).replace("\\r\\n","")[2:-1]
                if(len(line)> 0):
                    if(line.find(",")):
                        data = line.split(",")
                        self.dbC.insertData(data)
        except SerialException as se:
            print("Error al intentar abrir el puerto")
            print(se)

        except Exception as e:
            print("Error al intentar abrir el puerto")
            print(e)
        


def doc():
    print("Use solo serial2sql.py para guardar datos en la base de datos.")
    print("Si usa el parámetro -o, debe agregar el nombre del archivo donde desea guardar los datos.")
    print("Por favor revise la documentación: https://github.com/gsampallo/serial2sql")

if __name__ == "__main__":
    
    if (not os.path.exists("config.json")): 
        print("config.json no funciona.")
        doc()
        exit()
    else:
        if(len(sys.argv[1:]) == 0):   
            s = serial2sql("config.json")
        elif(sys.argv[1] == '-o'):
            if(len(sys.argv[1:]) >= 2):
                s = serial2sql("config.json")
                s.setOutput(sys.argv[2])
            else:
                print("Falta el archivo de salida")
                doc()
                exit()
        s.run()

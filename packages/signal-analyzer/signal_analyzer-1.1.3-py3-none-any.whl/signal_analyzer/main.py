import pyvisa
import time

class sg:

    def __init__(self,rm,addr) -> None:
        """
        Args: rm = pyvisa.ResourceManager() in args:
        """
        self.rm = rm
        self.addr = addr
        self.instr = None
        self.instr_id = None
        self.main_peak_power = None

    def open(self):
        try:
            self.instr = self.rm.open_resource(self.addr)
            time.sleep(1)
        except Exception:
            print("Failed to connect to Instrument.........")
            return

    def close(self):
        self.instr.close()

    def idn(self) -> str:
        """
        Returns: Instrument ID
        """
        self.open()
        self.instr_id = self.instr.query("*IDN?")
        self.close()
        return self.instr_id

    def __get_pK(self):
        """
        Returns [x,y] marker position
        """
        self.open()
        print("Waiting for Scan to finish....")
        time.sleep(12)
        self.instr.write("CALC:MARK1:MAX")
        marker_x_pos = float(self.instr.query("CALC:MARK1:X?"))/1000000000
        marker_y_pos = float(self.instr.query("CALC:MARK1:Y?"))
        self.close()
        return [marker_x_pos,marker_y_pos]

    def get_pk_pow(self,start,stop,rbw,vbw,x_or_y) -> float:
        """
        Args: start,stop,rbw,vbw,x_or_y
        Returns: Peak Power (dBm) or frequency (GHz)
        Note: x_or_y = (0,1) = (x,y)
        """
        self.open()
        self.instr.write("*CLS")
        self.instr.write(":FREQuency:START %s" % start)
        self.instr.write(":FREQuency:STOP %s" % stop)
        self.instr.write(":BANDwidth %s" % rbw)
        self.instr.write(":BANDwidth:Video %s" % vbw)
        peak_val = self.__get_pK()[x_or_y]
        self.main_peak_power = peak_val
        self.close()
        return peak_val

    def delta_pow(self,start,stop,rbw,vbw) -> float:
        """
        Args: start,stop,rbw,vbw
        Returns: Difference (peak_power)-(mian_peak_power)
        Note: To get Delta, you must run get_pk_pow() first.
        """
        self.open()
        self.instr.write("*CLS")
        self.instr.write(":FREQuency:START %s" % start)
        self.instr.write(":FREQuency:STOP %s" % stop)
        self.instr.write(":BANDwidth %s" % rbw)
        self.instr.write(":BANDwidth:Video %s" % vbw)
        peak_val = self.__get_pK()[1]
        delta_peak_val = (peak_val) - (self.main_peak_power)
        self.close()
        return delta_peak_val
    
    def recall_state(self,state) -> None:
        """
        Args: Pass State Number to Recall
        """
        self.open()
        self.instr.write(f"*RCL {state}")
        self.close()

class logging:
    
    def log(str,path):
        print(str)
        temp_file = path+'/log.txt'
        with open(temp_file,'a') as file:
            print(str, file=file)
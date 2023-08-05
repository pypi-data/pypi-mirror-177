idn() -> str:
        """
        Returns: Instrument ID
        """
-----------------------------------------------------------------------
__get_pK():
        """
        Returns [x,y] marker position
        """
-----------------------------------------------------------------------
get_pk_pow(start,stop,rbw,vbw,x_or_y):
        """
        Args: start,stop,rbw,vbw,x_or_y
        Returns: Peak Power (dBm) or frequency (GHz)
        Note: x_or_y = (0,1) = (x,y)
        """
-----------------------------------------------------------------------
delta_pow(start,stop,rbw,vbw):
        """
        Args: start,stop,rbw,vbw
        Returns: Difference (peak_power)-(mian_peak_power)
        Note: To get Delta, you must run get_pk_pow() first.
        """
-----------------------------------------------------------------------
recall_state(state):
        """
        Args: Pass State Number to Recall
        """
-----------------------------------------------------------------------

Example Use of this Module:

from signal_analyser import sg
from signal_analyser import logging


rm = pyvisa.ResourceManager()
signal_analyzer = sg(rm,"USB0::0x0957::0x0E0B::MY53030107::INSTR")
log = logging()
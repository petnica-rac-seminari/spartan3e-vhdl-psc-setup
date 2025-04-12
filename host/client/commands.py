
from serial import Serial
from serial.tools.list_ports import comports
from serial import PARITY_EVEN, PARITY_NONE, PARITY_ODD
from time import sleep
import sys 
from enum import Enum
from threading import Thread
from client.config import get_config_int, get_config_str
class Platform(Enum):
    WINDOWS = 1
    LINUX = 2
    MAC = 3
    UNKNOWN = 4
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

def get_platform():
    if sys.platform.startswith('win'):
        return Platform.WINDOWS
    elif sys.platform.startswith('linux'):
        return Platform.LINUX
    elif sys.platform.startswith('darwin'):
        return Platform.MAC
    else:
        return Platform.UNKNOWN
    
def get_serial_ports():
    """
    Get a list of serial ports available on the system.
    """
    if get_platform() == Platform.WINDOWS:
        return [port.device for port in comports() if 'COM' in port.device]
    elif get_platform() == Platform.LINUX:
        return [port.device for port in comports() if '/dev/ttyUSB' in port.device or '/dev/ttyACM' in port.device]
    elif get_platform() == Platform.MAC:
        return [port.device for port in comports() if '/dev/cu.' in port.device]
    else:
        raise Exception("Unsupported platform")
    
def get_serial_port(choice: str = None):
    """
    Get the serial port to use for communication.
    """
    configured_port = get_config_str("port", "Serial port to use", "")
    baudrate = get_config_int("baudrate", "Baudrate for serial port", 115200)
    parity = get_config_str("parity", "Parity for serial port", "N")
    stopbits = get_config_int("stopbits", "Stopbits for serial port", 1)
    bytesize = get_config_int("bytesize", "Bytesize for serial port", 8)
    timeout = get_config_int("timeout", "Timeout for serial port", 1)
    if parity == "N":
        parity = PARITY_NONE
    elif parity == "E":
        parity = PARITY_EVEN
    elif parity == "O":
        parity = PARITY_ODD
    else:
        raise Exception("Unsupported parity")
    ports = get_serial_ports()
    if len(ports) == 0:
        raise Exception("No serial ports found")
    elif len(ports) == 1:
        return Serial(ports[0], baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize, timeout=timeout)
    else:
        if choice is not None and choice != "":
            return Serial(choice, baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize, timeout=timeout)
        else:
            if configured_port != "":
                if configured_port in ports:
                    return Serial(configured_port, baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize, timeout=timeout)
                else:
                    print(f"Configured port {configured_port} not found in available ports")
            print("Available serial ports:")
            for i, port in enumerate(ports):
                print(f"{i}: {port}")
            choice = int(input("Select a serial port: "))
            myport = next(iter([port for i, port in enumerate(ports) if i == choice]), None)
            return Serial(myport, baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize, timeout=timeout)

class Commands:
    def list(self):
        return get_serial_ports()
    def get(self, *, port: str = ""):
        return get_serial_port(port)
    def pipe(self, *, port: str = ""):
        """
        Pipe the serial port to the console.
        """
        ser = get_serial_port(port)
        print(f"Connected to {ser.portstr}")
        # read from serial and write to stdout
        # write to serial from stdin 
        def read_from_serial():
            while True:
                data = ser.read()
                if data:
                    sys.stdout.write(data.decode())
                    sys.stdout.flush()
        def write_to_serial():
            while True:
                data = sys.stdin.read(1)
                if data:
                    ser.write(data.encode())
        # start threads to read and write
        read_thread = Thread(target=read_from_serial)
        write_thread = Thread(target=write_to_serial)
        read_thread.start()
        write_thread.start()
        read_thread.join()
        write_thread.join()
        ser.close()
        return True
    def read(self, *, port: str = ""):
        """
        Read from serial port and output to console
        """
        ser = get_serial_port(port)
        print(f"Connected to {ser.portstr}")
        # read from serial and write to stdout
        while True:
            data = ser.read()
            if data:
                sys.stdout.write(data.decode())
                sys.stdout.flush()
            else:
                break
        ser.close()
        return True
    def write(self, *, port: str = ""):
        """
        Write to serial port from stdin
        """
        ser = get_serial_port(port)
        print(f"Connected to {ser.portstr}")
        # write to serial from stdin 
        while True:
            data = sys.stdin.read(1)
            if data:
                ser.write(data.encode())
            else:
                break
        ser.close()
        return True
    def file(self, file: str, *, port: str = ""):
        """
        Send everything from file to serial and then output to console returned data
        """
        ser = get_serial_port(port)
        print(f"Connected to {ser.portstr}")
        # read from file and write to serial
        # write to serial from stdin 
        def read_from_file():
            with open(file, 'rb') as f:
                while True:
                    data = f.read(1)
                    if data:
                        ser.write(data)
                    else:
                        break
        def read_from_serial():
            while True:
                data = ser.read()
                if data:
                    sys.stdout.write(data.decode())
                    sys.stdout.flush()
        # start threads to read and write
        read_thread = Thread(target=read_from_file)
        write_thread = Thread(target=read_from_serial)
        read_thread.start()
        write_thread.start()
        read_thread.join()
        write_thread.join()
        ser.close()
        return True
    def bpipe(self, read_size: int, write_size: int, *, port: str = ""):
        """
        Send data block by block and send to serial 
        """
        ser = get_serial_port(port, baudrate)
        print(f"Connected to {ser.portstr}")
        while True:
            data = sys.stdin.read(write_size)
            if data:
                ser.write(data.encode())
                data = ser.read(read_size)
                if data:
                    sys.stdout.write(data.decode())
                    sys.stdout.flush()
            else:
                break
            data = ser.read(read_size)
            if data:
                sys.stdout.write(data.decode())
                sys.stdout.flush()
            else:
                break
        ser.close()
        return True

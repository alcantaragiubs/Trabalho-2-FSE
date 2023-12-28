import smbus2
import time

# Define some device parameters
I2C_ADDR = 0x27  # I2C device address

# Define some device constants
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command

LINE1 = 0x80  # 1st line
LINE2 = 0xC0  # 2nd line

LCD_BACKLIGHT = 0x08  # On
# LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100  # Enable bit

# Get I2C bus
bus = smbus2.SMBus(1)  # I2C bus number

# added functions
def lcd_init():
    lcd_byte(0x33, LCD_CMD)  # Initialise
    lcd_byte(0x32, LCD_CMD)  # Initialise
    lcd_byte(0x06, LCD_CMD)  # Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 0x0F On, Blink Off
    lcd_byte(0x28, LCD_CMD)  # Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # Clear display
    time.sleep(0.0005)

def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
    bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

    # High bits
    bus.write_byte(I2C_ADDR, bits_high)
    lcd_toggle_enable(bits_high)

    # Low bits
    bus.write_byte(I2C_ADDR, bits_low)
    lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
    # Toggle enable pin on LCD display
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(0.0005)

def lcdLoc(line):
    lcd_byte(line, LCD_CMD)

def ClrLcd():
    lcd_byte(0x01, LCD_CMD)
    lcd_byte(0x02, LCD_CMD)

def typeln(s):
    for char in s:
        lcd_byte(ord(char), LCD_CHR)

def typeChar(val):
    lcd_byte(ord(val), LCD_CHR)

def typeInt(i):
    typeln(str(i))

def typeFloat(myFloat):
    typeln("{:.2f}".format(myFloat))


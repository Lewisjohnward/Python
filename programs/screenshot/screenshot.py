"""
    Takes a screenshot and displays it 
"""
from PIL import Image
import mss



with mss.mss() as mss_instance: 
    monitor_1 = mss_instance.monitors[1]
    screenshot = mss_instance.grab(monitor_1)
    img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    img.show()

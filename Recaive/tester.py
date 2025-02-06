import os

folder_path = "/media/FSTUC/INTENSO"

if os.path.isdir(folder_path):
    print("Use INTENSO USB -Plastic")
elif os.path.isdir(r"/media/FSTUC/ESD-USB"):
    print("Use INTENSO USB -Grey")
else:
    print("No usb isnserted -> LOCAL LOGGING")
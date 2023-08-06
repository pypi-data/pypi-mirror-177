from PyQt6.QtCore import QSettings
ORGANIZATION_NAME = "Desk Helper"
APP_NAME = "Desk Helper"
setting = QSettings(ORGANIZATION_NAME, APP_NAME)
setting.clear()
if not setting.allKeys():
    print("Succeeded remove all settings.")
else:
    print("Removing all settings failed.")

import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Initialize USB HID Keyboard
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

# Delay allows USB driver enumeration after plug-in
time.sleep(4)

# Open Windows Run Dialog (Win + R)
kbd.send(Keycode.GUI, Keycode.R)
time.sleep(0.6)

# Launch PowerShell cleanly
layout.write("powershell\n")
time.sleep(1.2)

# Multi-drive security banner and volume inspection
commands = [
    "$Host.UI.RawUI.WindowTitle = 'PHYSICAL SECURITY AUDIT - ALL DRIVES'",
    "$Host.UI.RawUI.ForegroundColor = 'Red'",
    "Clear-Host",
    "Write-Host '==============================================================================' -ForegroundColor Red",
    "Write-Host '[!] SECURITY AUDIT ALERT: UNAUTHORIZED USB HID INJECTION DETECTED' -ForegroundColor Red",
    "Write-Host '==============================================================================' -ForegroundColor Red",
    "Write-Host '[i] Target Context : ' -NoNewline; Write-Host $env:USERNAME -ForegroundColor Yellow",
    "Write-Host '[i] Execution Scope: Full System (All Connected Volumes & Partitions)'",
    "Write-Host '[i] Attack Vector  : BadUSB Physical Keystroke Injection'",
    "Write-Host '------------------------------------------------------------------------------'",
    "Write-Host '[*] ENUMERATING ALL ACTIVE STORAGE DRIVES ACROSS SYSTEM:' -ForegroundColor Cyan",
    "Get-PSDrive -PSProvider FileSystem | ForEach-Object { Write-Host ('  [+] ' + \(_.Root + ' [ACCESSIBLE] - Free: ' + [math]::Round(\)_.Free/1GB, 2) + ' GB') -ForegroundColor Green }",
    "Write-Host '------------------------------------------------------------------------------'",
    "Write-Host '[*] DEFENSIVE REMEDIATION:' -ForegroundColor Yellow",
    "Write-Host '  1. Keystroke injection executes in user context across C:, D:, E:, and network drives.'",
    "Write-Host '  2. Enforce GPO USB device whitelisting by Hardware ID.'",
    "Write-Host '  3. Never plug untrusted hardware into any workstation.'",
    "Write-Host '==============================================================================' -ForegroundColor Red"
]

for cmd in commands:
    layout.write(cmd + "\n")
    time.sleep(0.05)
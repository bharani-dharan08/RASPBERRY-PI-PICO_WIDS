import network
import time
import rp2
from machine import Pin

# Set country code to initialize radio parameters ('US', 'IN', 'GB', etc.)
rp2.country('US')

led = Pin('LED', Pin.OUT)

TRUSTED_NETWORKS = {
    "Home_WiFi": ["a4:3e:51:12:99:80"]
}

SECURITY_MODES = {
    0: "OPEN", 1: "WEP", 2: "WPA-PSK", 3: "WPA2-PSK", 4: "WPA/WPA2-PSK", 5: "WPA3"
}

# --- CRITICAL FIX: CYW43 HARDWARE RESET & INITIALIZATION DELAY ---
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(0.5)
wlan.active(True)
time.sleep(1.5)  # Mandatory delay for CYW43 Wi-Fi hardware boot-up

def bssid_to_mac(bssid_bytes):
    return ":".join("{:02x}".format(b) for b in bssid_bytes)

def trigger_alert(threat_type, details):
    print("\n" + "="*50)
    print(f"[!!! SECURITY ALERT: {threat_type} !!!]")
    for key, val in details.items():
        print(f"  {key}: {val}")
    print("="*50 + "\n")
    
    for _ in range(10):
        led.value(1)
        time.sleep(0.1)
        led.value(0)
        time.sleep(0.1)

print("\n[+] Pico W WIDS Active via Terminal")
print("[+] Monitoring 2.4 GHz spectrum...\n")

scan_count = 0

while True:
    scan_count += 1
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    
    print(f"[*] Scan #{scan_count} running...", end="\r")
    
    try:
        scanned_aps = wlan.scan()
    except Exception as e:
        print(f"\n[-] Scan error: {e}. Resetting radio...")
        wlan.active(False)
        time.sleep(0.5)
        wlan.active(True)
        time.sleep(1.5)
        continue

    for ap in scanned_aps:
        ssid = ap[0].decode('utf-8', 'ignore').strip()
        bssid = bssid_to_mac(ap[1])
        channel = ap[2]
        rssi = ap[3]
        authmode = ap[4]
        sec_type = SECURITY_MODES.get(authmode, "UNKNOWN")

        if not ssid:
            continue

        if ssid in TRUSTED_NETWORKS:
            known_macs = [mac.lower() for mac in TRUSTED_NETWORKS[ssid]]
            
            if bssid.lower() not in known_macs:
                trigger_alert("EVIL TWIN ACCESS POINT", {
                    "Cloned SSID": ssid,
                    "Rogue MAC (BSSID)": bssid,
                    "Channel": channel,
                    "Signal Strength": f"{rssi} dBm",
                    "Security Profile": sec_type
                })
            elif authmode == 0:
                trigger_alert("UNENCRYPTED ROGUE AP (DOWNGRADE ATTACK)", {
                    "SSID": ssid,
                    "MAC Address": bssid
                })

    time.sleep(4)
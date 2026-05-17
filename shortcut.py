import os
import shutil
import keyboard

DESKTOP_PRIVATE = os.path.join(os.path.expanduser("~"), "Desktop")
DESKTOP_PUBLIC = r"C:\Users\Public\Desktop"

DESKTOPS = [d for d in [DESKTOP_PRIVATE, DESKTOP_PUBLIC] if os.path.exists(d)]

CACHE_FOLDER = os.path.join(DESKTOP_PRIVATE, ".hidden_shortcuts")

HOTKEY = "ctrl+shift+h"

LIGHT_BLUE = "\033[96m"
RESET = "\033[0m"

def hide_shortcuts():
    if not os.path.exists(CACHE_FOLDER):
        os.makedirs(CACHE_FOLDER)
        os.system(f'attrib +h "{CACHE_FOLDER}"')

    count = 0
    for desktop in DESKTOPS:
        for filename in os.listdir(desktop):
            if filename.endswith(".lnk") or filename.endswith(".url"):
                src = os.path.join(desktop, filename)
                
                if src == CACHE_FOLDER:
                    continue
                    
                prefix = "PUB_" if desktop == DESKTOP_PUBLIC else "PRI_"
                dst = os.path.join(CACHE_FOLDER, prefix + filename)
                
                try:
                    shutil.move(src, dst)
                    count += 1
                except Exception as e:
                    print(f"Error moving {filename}: {e}")
    
    if count > 0:
        print(f"[+] {count} shortcuts have been hidden.")
    else:
        print("[!] No shortcuts found to hide.")

def show_shortcuts():
    if not os.path.exists(CACHE_FOLDER):
        print("[!] No hidden shortcuts found.")
        return

    count = 0
    for filename in os.listdir(CACHE_FOLDER):
        src = os.path.join(CACHE_FOLDER, filename)
        
        if filename.startswith("PUB_"):
            real_filename = filename[4:]
            dst = os.path.join(DESKTOP_PUBLIC, real_filename)
        elif filename.startswith("PRI_"):
            real_filename = filename[4:]
            dst = os.path.join(DESKTOP_PRIVATE, real_filename)
        else:
            dst = os.path.join(DESKTOP_PRIVATE, filename)

        try:
            shutil.move(src, dst)
            count += 1
        except Exception as e:
            print(f"Error restoring {filename}: {e}")
            
    try:
        os.rmdir(CACHE_FOLDER)
    except OSError:
        pass

    if count > 0:
        print(f"[+] {count} shortcuts have been restored.")
    else:
        print("[!] No shortcuts found to restore.")

def toggle():
    print("\n[Action] Toggling shortcut visibility...")
    if os.path.exists(CACHE_FOLDER) and os.listdir(CACHE_FOLDER):
        show_shortcuts()
    else:
        hide_shortcuts()

if __name__ == "__main__":
    os.system("")

    print(LIGHT_BLUE + 
        "  _____ _    _  ____  _____ _______ _____ _    _ _______ \n"
        " / ____| |  | |/ __ \\|  __ \\__   __/ ____| |  | |__   __|\n"
        "| (___ | |__| | |  | | |__) | | | | |    | |  | |  | |   \n"
        " \\___ \\|  __  | |  | |  _  /  | | | |    | |  | |  | |   \n"
        " ____) | |  | | |__| | | \\ \\  | | | |____| |__| |  | |   \n"
        "|_____/|_|  |_|\\____/|_|  \\_\\ |_|  \\_____|\\____/   |_|   \n"
        + RESET
    )
    
    print("=" * 60)
    print(f"   Press {HOTKEY.upper()} to Hide / Show shortcuts")
    print("   Supports Public Desktop and Steam games.")
    print("=" * 60)
    print("Script is running... (Keep this window open)")

    keyboard.add_hotkey(HOTKEY, toggle)
    keyboard.wait()
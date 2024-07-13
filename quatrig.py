import pymem
import pymem.process
import keyboard
import time
from pynput.mouse import Controller, Button
from win32gui import GetWindowText, GetForegroundWindow
from random import uniform
import tkinter as tk
import threading

mouse = Controller()

dwEntityList = 26991960
dwLocalPlayerPawn = 25311752
m_iIDEntIndex = 5032
m_iTeamNum = 963
m_iHealth = 804

triggerKey = "shift"
is_running = False

def trigger_bot():
    global is_running
    print(f"[-] TriggerBot started.\n[-] Trigger key: {triggerKey.upper()}")
    pm = pymem.Pymem("cs2.exe")
    client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll

    while is_running:
        try:
            if GetWindowText(GetForegroundWindow()) != "Counter-Strike 2":
                time.sleep(0.1)
                continue

            if keyboard.is_pressed(triggerKey):
                player = pm.read_longlong(client + dwLocalPlayerPawn)
                entityId = pm.read_int(player + m_iIDEntIndex)

                if entityId > 0:
                    entList = pm.read_longlong(client + dwEntityList)

                    entEntry = pm.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
                    entity = pm.read_longlong(entEntry + 120 * (entityId & 0x1FF))

                    entityTeam = pm.read_int(entity + m_iTeamNum)
                    playerTeam = pm.read_int(player + m_iTeamNum)

                    if entityTeam != playerTeam:
                        entityHp = pm.read_int(entity + m_iHealth)
                        if entityHp > 0:
                            time.sleep(uniform(0.01, 0.03))
                            mouse.press(Button.left)
                            time.sleep(uniform(0.01, 0.05))
                            mouse.release(Button.left)

                time.sleep(0.03)
            else:
                time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(0.1)

def start_trigger_bot():
    global is_running
    is_running = True
    bot_thread = threading.Thread(target=trigger_bot)
    bot_thread.start()

def stop_trigger_bot():
    global is_running
    is_running = False

def toggle_trigger_bot():
    if start_button.config('text')[-1] == 'Start':
        start_button.config(text='Stop')
        start_trigger_bot()
    else:
        start_button.config(text='Start')
        stop_trigger_bot()

app = tk.Tk()
app.title("TriggerBot GUI")

frame = tk.Frame(app, padx=10, pady=10)
frame.pack(pady=10)

start_button = tk.Button(frame, text="Start", width=15, command=toggle_trigger_bot)
start_button.pack(pady=5)

quit_button = tk.Button(frame, text="Quit", width=15, command=app.quit)
quit_button.pack(pady=5)

app.mainloop()

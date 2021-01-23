import keyboard, time, pymem, re, os, colorama, psutil, sys, itertools, threading, json
import pypresence

colorama.init(convert=True)

end = False

# Cheat Switches
bhopSwitch = False
noflashSwitch = False
glowSwitch = False
radarSwitch = False
triggerbotSwitch = False
rcsSwitch = False
# chamsSwitch = False
moneySwitch = False
wallSwitch = False

# Cheat keybindings
bhopKeybind = "F1"
wallKeybind = "F2"
noflashKeybind = "F3"
glowKeybind = "F4"
radarKeybind = "F6"
triggerbotKeybind = "F7"
rcsKeybind = "F8"
# chamsKeybind = "F8"
moneyKeybind = "F8"

# Cheat settings
is_in_game = False
buttonsPressed = []

teamGlow = False
healthBasedGlow = False

# teamChams = True
# healthBasedChams = False

tRGBAGlow = (0, 0, 255, 255)
ctRGBAGlow = (255, 0, 0, 255)


# tRGBChams = (0, 0, 255)
# ctRGBChams = (255, 0, 0)
# chamsBrightness = 50


# Console updater etc
class console():
    def printBanner(self):
        print(colorama.Fore.MAGENTA + """███████╗██╗   ██╗██████╗ ██████╗ ██████╗  ██████╗ 
██╔════╝██║   ██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
███████╗██║   ██║██████╔╝██████╔╝██████╔╝██║   ██║
╚════██║██║   ██║██╔═══╝ ██╔══██╗██╔══██╗██║   ██║
███████║╚██████╔╝██║     ██████╔╝██║  ██║╚██████╔╝
╚══════╝ ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
                                                """)

    def updateConsole(self):
        os.system("cls")
        self.printBanner()
        keybindings = [bhopKeybind, wallKeybind, noflashKeybind, glowKeybind, radarKeybind, triggerbotKeybind,
                       rcsKeybind, moneyKeybind]
        misc = [bhopSwitch, wallSwitch, noflashSwitch, glowSwitch, radarSwitch, triggerbotSwitch, rcsSwitch,
                moneySwitch]
        name = ["Bhop", "Wallhack", "No flash", "Glow", "Radar", "Triggerbot", "RCS", "Money hack"]
        for num, x in enumerate(misc):
            print(colorama.Fore.CYAN + name[num] + f'({keybindings[num]}): ', end="")
            # try:
            #     val = int(x)
            #     is_int = True
            # except:
            #     is_int = False
            #
            # if not is_int:
            print(f"{colorama.Fore.GREEN}ON" if x else f"{colorama.Fore.LIGHTRED_EX}OFF")
            # else:
            #     print(colorama.Fore.RESET + str(x))
        print(colorama.Fore.CYAN + "Reload config(F12)")


terminal = console()


def reloadConfig():
    with open('config.json') as f:
        config = json.load(f)

    global bhopKeybind
    global noflashKeybind
    global glowKeybind
    global radarKeybind
    global triggerbotKeybind
    global rcsKeybind
    global moneyKeybind
    global teamGlow
    global healthBasedGlow
    global tRGBAGlow
    global ctRGBAGlow

    # Cheat keybindings
    bhopKeybind = config["bhopKeybind"]
    noflashKeybind = config["noflashKeybind"]
    glowKeybind = config["glowKeybind"]
    radarKeybind = config["radarKeybind"]
    triggerbotKeybind = config["triggerbotKeybind"]
    rcsKeybind = config["rcsKeybind"]
    # chamsKeybind = "F8"
    moneyKeybind = config["moneyKeybind"]

    # Cheat settings
    teamGlow = config["teamGlow"]
    healthBasedGlow = config["healthBasedGlow"]

    tRGBAGlow = config["tRGBAGlow"]
    ctRGBAGlow = config["ctRGBAGlow"]


# Cheat functions
# hook into game and init client and engine
def hookAndInit():
    global pm
    global client
    global clientBase
    global engine
    global engineBase
    terminal.printBanner()
    print(colorama.Fore.CYAN + "Make sure Csgo is opened!")
    time.sleep(1.5)
    fini = False
    is_error = True
    while not fini:
        for proc in psutil.process_iter():
            try:
                if "csgo" in proc.name().lower():
                    while True:
                        try:
                            os.system("cls")
                            pm = pymem.Pymem("csgo.exe")
                            os.system("cls")
                            fini = True
                            break
                        except (pymem.exception.ProcessNotFound, AttributeError):
                            pass
                        time.sleep(1)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    while is_error:
        try:
            client = pymem.process.module_from_name(pm.process_handle, "client.dll")
            clientBase = client.lpBaseOfDll
            engine = pymem.process.module_from_name(pm.process_handle, "engine.dll")
            engineBase = engine.lpBaseOfDll
            is_error = False
        except:
            pass
        time.sleep(1)
    getOffsets()


# Get offset from pattern
def get_sig(module, pattern, extra: int = 0, offset: int = 0, relative: bool = True):
    bytes = pm.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    non_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra
    is_relative = pm.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return "0x{:X}".format(is_relative) if relative else "0x{:X}".format(non_relative)


# Get offsets
def getOffsets():
    os.system("cls")
    print(colorama.Fore.GREEN)
    done = False

    def animate():
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done:
                break
            sys.stdout.write('\rGetting offsets ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write('\rDone!     ')

    animation = threading.Thread(target=animate)
    animation.start()

    # Get offsets needed
    global dwClientState
    global dwClientState_State
    global dwLocalPlayer
    global dwEntityList
    global dwForceJump
    global m_flFlashMaxAlpha
    global m_fFlags
    global m_iObserverMode
    global dwForceAttack
    global dwGlowObjectManager
    global m_iTeamNum
    global m_iGlowIndex
    global m_bSpotted
    global m_iCrosshairId
    global m_aimPunchAngle
    global dwClientState_ViewAngles
    global m_iShotsFired
    global m_iHealth
    global m_clrRender
    global model_ambient_min
    global m_money
    global m_drawOtherModels

    dwClientState = int(get_sig(engine, rb"\xA1....\x33\xD2\x6A\x00\x6A\x00\x33\xC9\x89\xB0", 0, 1), 0)
    dwClientState_State = int(get_sig(engine, rb"\x83\xB8.....\x0F\x94\xC0\xC3", 0, 2, False), 0)
    dwLocalPlayer = int(get_sig(client, rb"\x8D\x34\x85....\x89\x15....\x8B\x41\x08\x8B\x48\x04\x83\xF9\xFF", 4, 3), 0)
    dwEntityList = int(get_sig(client, rb"\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8", 0, 1), 0)
    dwForceJump = int(get_sig(client, rb"\x8B\x0D....\x8B\xD6\x8B\xC1\x83\xCA\x02", 0, 2), 0)
    dwForceAttack = int(get_sig(client, rb"\x89\x0D....\x8B\x0D....\x8B\xF2\x8B\xC1\x83\xCE\x04", 0, 2), 0)
    dwGlowObjectManager = int(get_sig(client, rb"\xA1....\xA8\x01\x75\x4B", 4, 1), 0)
    dwClientState_ViewAngles = int(get_sig(engine, rb"\xF3\x0F\x11\x80....\xD9\x46\x04\xD9\x05", 0, 4, False), 0)
    m_money = re.search(rb".\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF",
                        pm.read_bytes(clientBase, client.SizeOfImage)).start()
    m_drawOtherModels = re.search(rb"\x83\xF8.\x8B\x45\x08\x0F",
                                  pm.read_bytes(clientBase, client.SizeOfImage)).start() + 2

    m_flFlashMaxAlpha = (0xA41C)
    m_iTeamNum = (0xF4)
    m_iGlowIndex = (0xA438)
    m_fFlags = (0x104)
    m_iObserverMode = (0x3378)
    m_bSpotted = (0x93D)
    m_iCrosshairId = (0xB3E4)
    m_aimPunchAngle = (0x302C)
    m_iShotsFired = (0xA390)
    m_iHealth = (0x100)
    m_clrRender = (0x70)
    model_ambient_min = (0x59105C)

    done = True
    print("")
    print(colorama.Fore.RESET)
    time.sleep(0.1)
    print("")


# Bhop
def bhop():
    ForceJump = clientBase + dwForceJump
    grounds = [257, 263]
    while True:
        if is_in_game:
            on_ground = pm.read_int(LocalPlayer + m_fFlags)
            if on_ground in grounds and keyboard.is_pressed("space"):
                pm.write_int(ForceJump, 5)
                time.sleep(0.08)
                pm.write_int(ForceJump, 4)
            else:
                time.sleep(0.01)
        if bhopSwitch == False or end:
            return


# No flash
def noFlash():
    flash = LocalPlayer + m_flFlashMaxAlpha
    while True:
        if is_in_game:
            pm.write_float(flash, float(0))
        if noflashSwitch == False or end:
            return


# Do glow on given entity
def doGlow(rgba, entity_glow, GlowObjectManager, entity):
    pm.write_float(GlowObjectManager + entity_glow * 0x38 + 0x4,
                   float(rgba[0] / 255) if not healthBasedGlow else float(
                       ((255 - int(pm.read_int(entity + m_iHealth) * 2.55)) / 255)))  # R
    pm.write_float(GlowObjectManager + entity_glow * 0x38 + 0x8, float(rgba[1] / 255))  # G
    pm.write_float(GlowObjectManager + entity_glow * 0x38 + 0xC,
                   float(rgba[2] / 255) if not healthBasedGlow else float(
                       (int(pm.read_int(entity + m_iHealth) * 2.55) / 255)))  # B
    pm.write_float(GlowObjectManager + entity_glow * 0x38 + 0x10, float(rgba[3] / 255))  # A
    pm.write_int(GlowObjectManager + entity_glow * 0x38 + 0x24, 1)


# Glow
def glow():
    GlowObjectManager = pm.read_int(clientBase + dwGlowObjectManager)
    while True:
        if is_in_game:
            for i in range(1, 32):
                entity = pm.read_int(clientBase + dwEntityList + i * 0x10)

                if entity:
                    entity_team_id = pm.read_int(entity + m_iTeamNum)
                    entity_glow = pm.read_int(entity + m_iGlowIndex)
                    localTeam = pm.read_int(LocalPlayer + m_iTeamNum)
                    try:

                        if teamGlow:
                            if entity_team_id == 2:
                                doGlow(tRGBAGlow, entity_glow, GlowObjectManager, entity)
                            if entity_team_id == 3:
                                doGlow(ctRGBAGlow, entity_glow, GlowObjectManager, entity)
                        else:
                            if localTeam == 3:
                                if entity_team_id == 2:
                                    doGlow(tRGBAGlow, entity_glow, GlowObjectManager, entity)
                            else:
                                if entity_team_id == 3:
                                    doGlow(ctRGBAGlow, entity_glow, GlowObjectManager, entity)
                    except:
                        continue
            time.sleep(0.0005)
        if glowSwitch == False or end:
            return


# def doChams(rgb, entity):
#     pm.write_int(entity + m_clrRender, rgb[0])  # R
#     pm.write_int(entity + m_clrRender + 0x1, rgb[1])  # G
#     pm.write_int(entity + m_clrRender + 0x2, rgb[2])  # b
#
#
#
# def chams():
#     while True:
#         if is_in_game:
#             for i in range(1, 32):
#                 entity = pm.read_int(clientBase + dwEntityList + i * 0x10)
#
#                 if entity:
#                     entity_team_id = pm.read_int(entity + m_iTeamNum)
#                     localTeam = pm.read_int(LocalPlayer + m_iTeamNum)
#                     try:
#                         if teamGlow:
#                             if entity_team_id == 2:
#                                 doChams(tRGBChams, entity)
#                             if entity_team_id == 3:
#                                 doChams(ctRGBChams, entity)
#                         else:
#                             if localTeam == 3:
#                                 if entity_team_id == 2:
#                                     doChams(tRGBChams, entity)
#                             else:
#                                 if entity_team_id == 3:
#                                     doChams(ctRGBChams, entity)
#                     except:
#                         continue
#             # brightnessPtr = engineBase + model_ambient_min - 0x2c
#             # xored = float(chamsBrightness) ^ brightnessPtr
#             # pm.write_int(engineBase + model_ambient_min, xored)
#             time.sleep(0.0005)
#         if chamsSwitch == False or end:
#             return

# Radar
def radar():
    while True:
        for i in range(1, 32):
            entity = pm.read_int(clientBase + dwEntityList + i * 0x10)
            if entity:
                pm.write_uchar(entity + m_bSpotted, 1)
        if radarSwitch == False or end:
            return


# Triggerbot
def triggerbot():
    while True:
        try:
            crosshairID = pm.read_int(LocalPlayer + m_iCrosshairId)
            getTeam = pm.read_int(clientBase + dwEntityList + (crosshairID - 1) * 0x10)
            localTeam = pm.read_int(LocalPlayer + m_iTeamNum)
            crosshairTeam = pm.read_int(getTeam + m_iTeamNum)
        except:
            continue

        if crosshairID > 0 and crosshairID <= 31 and localTeam != crosshairTeam:
            pm.write_int(clientBase + dwForceAttack, 6)
            time.sleep(0.01)

        if triggerbotSwitch == False or end:
            return


# RCS - Recoil Control System
def rcs():
    old_aim_punch_x = old_aim_punch_y = 0
    while True:
        Punch_x = pm.read_float(LocalPlayer + m_aimPunchAngle)
        Punch_y = pm.read_float(LocalPlayer + m_aimPunchAngle + 0x4)
        ShotsFired = pm.read_int(LocalPlayer + m_iShotsFired)

        if ShotsFired >= 1:
            ClientState = pm.read_int(engineBase + dwClientState)
            curr_view_angles_x = pm.read_float(ClientState + dwClientState_ViewAngles)
            curr_view_angles_y = pm.read_float(ClientState + dwClientState_ViewAngles + 0x4)
            new_view_angles_x = ((curr_view_angles_x + old_aim_punch_x) - (Punch_x * float(2)))
            new_view_angles_y = ((curr_view_angles_y + old_aim_punch_y) - (Punch_y * float(2)))

            while new_view_angles_y > 180:
                new_view_angles_y -= 360

            while new_view_angles_y < -180:
                new_view_angles_y += 360

            if new_view_angles_x > 89.0:
                new_view_angles_x = 89.0

            if new_view_angles_x < -89.0:
                new_view_angles_x = -89.0

            old_aim_punch_x = Punch_x * float(2)
            old_aim_punch_y = Punch_y * float(2)

            pm.write_float(ClientState + dwClientState_ViewAngles, new_view_angles_x)
            pm.write_float(ClientState + dwClientState_ViewAngles + 0x4, new_view_angles_y)
        else:
            old_aim_punch_x = old_aim_punch_y = 0
        time.sleep(0.001)

        if rcsSwitch == False or end:
            return


# Show enemy's money
def moneyHack():
    money = clientBase + m_money
    while True:
        if is_in_game:
            pm.write_uchar(money, 0xEB if pm.read_uchar(money) == 0x75 else 0x75)
            break
        else:
            time.sleep(0.01)

# enable r_drawOtherModels 2
def wallHack():
    wall = clientBase + m_drawOtherModels
    while True:
        if is_in_game:
            pm.write_uchar(wall, 2 if pm.read_uchar(wall) == 1 else 1)
            break
        else:
            time.sleep(0.01)


# Check if in game
def inGame():
    ClientState = pm.read_int(engineBase + dwClientState)
    return True if pm.read_int(ClientState + dwClientState_State) == 6 else False


# Stop the cheat
def endCheat(error=False):
    end = True
    if error:
        os.system("cls")
        print(colorama.Fore.RED + """▓█████  ██▀███   ██▀███   ▒█████   ██▀███  
▓█   ▀ ▓██ ▒ ██▒▓██ ▒ ██▒▒██▒  ██▒▓██ ▒ ██▒
▒███   ▓██ ░▄█ ▒▓██ ░▄█ ▒▒██░  ██▒▓██ ░▄█ ▒
▒▓█  ▄ ▒██▀▀█▄  ▒██▀▀█▄  ▒██   ██░▒██▀▀█▄  
░▒████▒░██▓ ▒██▒░██▓ ▒██▒░ ████▓▒░░██▓ ▒██▒
░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒▓ ░▒▓░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░
 ░ ░  ░  ░▒ ░ ▒░  ░▒ ░ ▒░  ░ ▒ ▒░   ░▒ ░ ▒░
   ░     ░░   ░   ░░   ░ ░ ░ ░ ▒    ░░   ░ 
   ░  ░   ░        ░         ░ ░     ░     
                                                """)
        print(colorama.Fore.YELLOW + "\r You closed CSGO.exe")
    else:
        os.system("cls")
        print(colorama.Fore.YELLOW + "\r Cheat stopped")
    time.sleep(2)
    pm.close_process()
    sys.exit()


# Load discord presence
RPC = pypresence.Presence(780405348418715668)
RPC.connect()
RPC.update(large_image="supbro", large_text="Flossless", details="Playing like a boss", state="Atacc!!",
           start=time.time(), end=None)

# Start cheat
hookAndInit()
os.system("cls")
terminal.updateConsole()

# Main loop
try:
    while True:
        is_in_game = inGame()
        if is_in_game:
            LocalPlayer = pm.read_int(clientBase + dwLocalPlayer)
        if keyboard.is_pressed(bhopKeybind) and bhopKeybind not in buttonsPressed:
            buttonsPressed.append(bhopKeybind)
            if not bhopSwitch:
                threading.Thread(target=bhop).start()
            bhopSwitch = not bhopSwitch
            terminal.updateConsole()
        elif bhopKeybind in buttonsPressed and not keyboard.is_pressed(bhopKeybind):
            buttonsPressed.remove(bhopKeybind)

        if keyboard.is_pressed(wallKeybind) and wallKeybind not in buttonsPressed:
            buttonsPressed.append(wallKeybind)
            threading.Thread(target=wallHack).start()
            wallSwitch = not wallSwitch
            terminal.updateConsole()
        elif moneyKeybind in buttonsPressed and not keyboard.is_pressed(moneyKeybind):
            buttonsPressed.remove(moneyKeybind)
        if keyboard.is_pressed(noflashKeybind) and noflashKeybind not in buttonsPressed:
            buttonsPressed.append(noflashKeybind)
            threading.Thread(target=noFlash).start()
            noflashSwitch = not noflashSwitch
            terminal.updateConsole()
        elif noflashKeybind in buttonsPressed and not keyboard.is_pressed(noflashKeybind):
            buttonsPressed.remove(noflashKeybind)

        if keyboard.is_pressed(glowKeybind) and glowKeybind not in buttonsPressed:
            buttonsPressed.append(glowKeybind)
            if not glowSwitch:
                threading.Thread(target=glow).start()
            glowSwitch = not glowSwitch
            terminal.updateConsole()
        elif glowKeybind in buttonsPressed and not keyboard.is_pressed(glowKeybind):
            buttonsPressed.remove(glowKeybind)

        if keyboard.is_pressed(radarKeybind) and radarKeybind not in buttonsPressed:
            buttonsPressed.append(radarKeybind)
            if not radarSwitch:
                threading.Thread(target=radar).start()
            radarSwitch = not radarSwitch
            terminal.updateConsole()
        elif radarKeybind in buttonsPressed and not keyboard.is_pressed(radarKeybind):
            buttonsPressed.remove(radarKeybind)

        if keyboard.is_pressed(triggerbotKeybind) and triggerbotKeybind not in buttonsPressed:
            buttonsPressed.append(triggerbotKeybind)
            if not triggerbotSwitch:
                threading.Thread(target=triggerbot).start()
            triggerbotSwitch = not triggerbotSwitch
            terminal.updateConsole()
        elif triggerbotKeybind in buttonsPressed and not keyboard.is_pressed(triggerbotKeybind):
            buttonsPressed.remove(triggerbotKeybind)

        if keyboard.is_pressed(rcsKeybind) and rcsKeybind not in buttonsPressed:
            buttonsPressed.append(rcsKeybind)
            if not rcsSwitch:
                threading.Thread(target=rcs).start()
            rcsSwitch = not rcsSwitch
            terminal.updateConsole()
        elif rcsKeybind in buttonsPressed and not keyboard.is_pressed(rcsKeybind):
            buttonsPressed.remove(rcsKeybind)

        # if keyboard.is_pressed("F8") and "F8" not in buttonsPressed:
        #     buttonsPressed.append("F8")
        #     if not chamsSwitch:
        #         threading.Thread(target=chams).start()
        #     chamsSwitch = not chamsSwitch
        #     terminal.updateConsole()
        # elif "F8" in buttonsPressed and not keyboard.is_pressed("F8"):
        #     buttonsPressed.remove("F8")

        if keyboard.is_pressed(moneyKeybind) and moneyKeybind not in buttonsPressed:
            buttonsPressed.append(moneyKeybind)
            threading.Thread(target=moneyHack).start()
            moneySwitch = not moneySwitch
            terminal.updateConsole()
        elif moneyKeybind in buttonsPressed and not keyboard.is_pressed(moneyKeybind):
            buttonsPressed.remove(moneyKeybind)

        if keyboard.is_pressed("F12") and "F12" not in buttonsPressed:
            buttonsPressed.append("F12")
            threading.Thread(target=reloadConfig).start()
        elif moneyKeybind in buttonsPressed and not keyboard.is_pressed(moneyKeybind):
            buttonsPressed.remove(moneyKeybind)

        if keyboard.is_pressed("end"):
            endCheat()
        time.sleep(0.01)
        
except pymem.exception.MemoryReadError:
    endCheat(error=True)

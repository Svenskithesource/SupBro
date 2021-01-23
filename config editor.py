from dearpygui.core import *
from dearpygui.simple import *
import json

def saveConfig(sender, data):
    with open('config.json', "r") as f:
        config = json.load(f)
    # Cheat keybindings
    config["bhopKeybind"] = get_value("bhopkeybind")
    config["noflashKeybind"] = get_value("noflashkeybind")
    config["glowKeybind"] = get_value("glowkeybind")
    config["radarKeybind"] = get_value("radarkeybind")
    config["triggerbotKeybind"] = get_value("triggerbotkeybind")
    config["rcsKeybind"] = get_value("rcskeybind")
    config["moneyKeybind"] = get_value("moneykeybind")

    # Cheat settings
    config["teamGlow"] = get_value("teamglow")
    config["healthBasedGlow"] = get_value("healthbasedglow")

    config["tRGBAGlow"] = get_value("tchams")
    config["ctRGBAGlow"] = get_value("ctchams")

    with open('config.json', "w") as f:
        json.dump(config, f, indent=4)

def reloadConfig(data, sender):
    with open('config.json', "r") as f:
        config = json.load(f)
    # Cheat keybindings
    set_value("bhopkeybind", config["bhopKeybind"])
    set_value("noflashkeybind", config["noflashKeybind"])
    set_value("glowkeybind", config["glowKeybind"])
    set_value("radarkeybind", config["radarKeybind"])
    set_value("triggerbotkeybind", config["triggerbotKeybind"])
    set_value("rcskeybind", config["rcsKeybind"])
    set_value("moneykeybind", config["moneyKeybind"])

    # Cheat settings
    set_value("teamglow", config["teamGlow"])
    set_value("healthbasedglow", config["healthBasedGlow"])

    set_value("tchams", list(config["tRGBAGlow"]))
    set_value("ctchams", list(config["ctRGBAGlow"]))

with window("Main Window", menubar=False):
    add_text("Chams")
    add_color_edit4("Terrorists color", source="tchams", no_inputs=True)
    add_color_edit4("Counter Terrorists color", source="ctchams", no_inputs=True)
    add_checkbox("Health based glow", source="healthbasedglow")
    add_checkbox("Teammate glow", source="teamglow")
    add_spacing(count=3)
    add_text("Keybind")
    add_input_text("Bhop", source="bhopkeybind", width=50)
    add_input_text("No flash", source="noflashkeybind", width=50)
    add_input_text("Glow", source="glowkeybind", width=50)
    add_input_text("Radar hack", source="radarkeybind", width=50)
    add_input_text("Triggerbot", source="triggerbotkeybind", width=50)
    add_input_text("RCS", source="rcskeybind", width=50)
    add_input_text("Money hack", source="moneykeybind", width=50)
    add_button("Save config", callback=saveConfig)
    add_button("Reload config", callback=reloadConfig)
    reloadConfig("t", "t")

set_main_window_title("Supbro")
start_dearpygui(primary_window="Main Window")
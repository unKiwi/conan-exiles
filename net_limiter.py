from config import INPUT_SPEED_LIMIT, OUTPUT_SPEED_LIMIT
import pyshaper
import keyboard
from global_variables import network_is_limited

app_name = "nom_de_l_application"
shaper = pyshaper.TCShaper()
iface = pyshaper.get_default_iface()
shaper.add_interface(iface)
class_rule = pyshaper.ClassRule(app_name, parent=shaper.root)

def limit_bandwidth():
    class_rule.add_child(pyshaper.LeafRule("rate", str(INPUT_SPEED_LIMIT) + "bps"))
    class_rule.add_child(pyshaper.LeafRule("rate", str(OUTPUT_SPEED_LIMIT) + "bps", direction="outgoing"))

    shaper.compile()

    print("bandwidth limited")

def remove_bandwidth_limit():
    class_rule.delete()
    shaper.compile()

    print("bandwidth no longer limited")

def toggle_bandwidth_limit():
    network_is_limited = not network_is_limited
    if network_is_limited:
        limit_bandwidth()
    else:
        remove_bandwidth_limit()

keyboard.on_press_key("t", lambda _: toggle_bandwidth_limit())
keyboard.wait("esc")

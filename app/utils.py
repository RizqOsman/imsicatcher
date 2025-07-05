import subprocess

def estimate_distance(rssi: float, tx_power: float = 30.0, path_loss_exponent: float = 2.5) -> float:
    if rssi is None:
        return -1.0
    try:
        return round(10 ** ((tx_power - abs(rssi)) / (10 * path_loss_exponent)), 2)
    except Exception:
        return -1.0

def scan_bts_arfcn() -> list[str]:
    try:
        output = subprocess.check_output(["kal", "-s", "GSM900"], stderr=subprocess.STDOUT, timeout=15)
        lines = output.decode().splitlines()
        arfcn_list = [line for line in lines if "chan:" in line]
        return arfcn_list
    except Exception as e:
        return [f"Error: {e}"]
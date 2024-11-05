import time
import json
import ipykernel
    
def check_kernel():
    kernel_id = ipykernel.connect.get_connection_file()

    with open(kernel_id, 'r') as f:
        data = json.load(f)  

    if data["kernel_name"] == "":
        print("Select kernel first!")
    else:
        print(f"Kernel: {data['kernel_name']}")


def format_timespan(seconds):
    hours = seconds // 3600
    minutes = (seconds - hours*3600) // 60
    remaining_seconds = seconds - hours*3600 - minutes*60
    timespan = f"{hours} hours {minutes} minutes {remaining_seconds:.4f} seconds."
    return timespan
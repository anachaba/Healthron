scan_val = 0
def scan_val_controller():
    global scan_val
    while True:

        for i in range(0,8,1):
            scan_val = i
            print(scan_val)
        for i in range(8,0,-1):
            scan_val = i
            print(scan_val)

scan_val_controller()
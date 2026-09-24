from plateloader import PlateLoader

VALID_POSITIONS = ["1", "2", "3", "4", "5"]

if __name__ == "__main__":
    print("Serial Menu")
    plateloader = PlateLoader(port="/dev/ttyACM0")
    plateloader.connect()
    try:
        while True:
            print("\n\n0. Exit")
            print("1. RESET")
            print("2. X-AXIS")
            print("3. MOVE")
            print("4. GRIPPER")
            print("5. Z-AXIS")
            print("6. LOADER_STATUS")
            selection = input("Make a selection: ")

            if selection == "0":
                break
            elif selection == "1":
                response = plateloader.send_command("RESET")
            elif selection == "2":
                to_where = input("Enter X-AXIS position (1-5): ")
                if to_where not in VALID_POSITIONS:
                    print("Invalid X-AXIS position", to_where)
                    continue
                response = plateloader.send_command(f"X-AXIS {to_where}")
            elif selection == "3":
                from_where = input("Enter MOVE from position (1-5): ")
                to_where = input("Enter MOVE to position (1-5): ")
                if from_where not in VALID_POSITIONS or to_where not in VALID_POSITIONS:
                    print("Invalid MOVE positions", from_where, to_where)
                    continue
                response = plateloader.send_command(f"MOVE {from_where} {to_where}")
            elif selection == "4":
                state = input("Enter GRIPPER state (0 = Open, 1 = Close): ")
                if state == "0":
                    response = plateloader.send_command("GRIPPER OPEN")
                elif state == "1":
                    response = plateloader.send_command("GRIPPER CLOSE")
                else:
                    print("Invalid GRIPPER state", state)
                    continue
            elif selection == "5":
                state = input("Enter Z-AXIS state (0 = Retract, 1 = Extend): ")
                if state == "0":
                    response = plateloader.send_command("Z-AXIS RETRACT")
                elif state == "1":
                    response = plateloader.send_command("Z-AXIS EXTEND")
                else:
                    print("Invalid Z-AXIS state", state)
                    continue
            elif selection == "6":
                response = plateloader.send_command("LOADER_STATUS")
            else:
                print("Invalid selection", selection)
                continue
            
            print("Response:", response)
    finally:
        plateloader.disconnect()  # Ensure cleanup
        print("Goodbye!")

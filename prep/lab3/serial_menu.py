from plateloader import PlateLoader

if __name__ == "__main__":
    print("Testing PlateLoader")
    plateloader = PlateLoader(port="/dev/ttyACM0")
    plateloader.connect()
    try:
        while True:
            print("\n\n0. Exit")
            print("1. RESET")
            print("2. X-AXIS")
            selection = input("Make a selection: ")

            if selection == "0":
                break
            elif selection == "1":
                response = plateloader.send_command("RESET")
            elif selection == "2":
                to_where = input("Enter X-AXIS position: ")
                response = plateloader.send_command(f"X-AXIS {to_where}")
            else:
                print("Invalid selection", selection)
                continue
            
            print("Response:", response)
    finally:
        plateloader.disconnect()  # Ensure cleanup
        print("Goodbye!")



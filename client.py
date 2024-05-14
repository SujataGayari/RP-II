import requests
# Function to check parking spot availability
def check_availability():
    try:
        # Prompt the user to enter the location
        location = input("Enter the location (A, B, or C): ").upper()
        # Send a GET request to the server
        response = requests.get(f'http://127.0.0.1:5000/check_availability?location={location}')
        data = response.json()
        # Process the response
        if 'available_spots' in data:
            print(f'Available parking spots at location {location}: {data["available_spots"]}')
        else:
            print('Error:', data.get('error', 'Unknown error'))
    except Exception as e:
        print('Error:', str(e))
# Function to occupy a parking spot
def occupy_parking_spot():
    try:
        # Prompt the user to enter the location
        location = input("Enter the location (A, B, or C): ").upper()
        # Send a GET request to check available spots
        response = requests.get(f'http://127.0.0.1:5000/check_availability?location={location}')
        data = response.json()
        if 'available_spots' in data:
            print(f'Available parking spots at location {location}: {data["available_spots"]}')
            # Ask the user to choose a parking spot
            spot_number = input("Enter the parking spot number to occupy: ")
            # Send a POST request to the server to occupy the selected parking spot
            response = requests.post('http://127.0.0.1:5000/occupy_spot', json={'location': location, 'spot_number': spot_number})
            data = response.json()
            # Process the response
            if 'message' in data:
                print(data['message'])
            else:
                print('Error:', data.get('error', 'Unknown error'))
        else:
            print('Error:', data.get('error', 'Unknown error'))
    except Exception as e:
        print('Error:', str(e))
# Function to leave a parking spot
def leave_parking_spot():
    try:
        # Prompt the user to enter the location
        location = input("Enter the location (A, B, or C): ").upper()
        # Send a GET request to check available spots
        response = requests.get(f'http://127.0.0.1:5000/check_availability?location={location}')
        data = response.json()
        if 'available_spots' in data:
            print(f'Available parking spots at location {location}: {data["available_spots"]}')
            # Ask the user to enter the parking spot number they are leaving
            spot_number = input("Enter the parking spot number to leave: ")
            # Send a POST request to the server to leave the selected parking spot
            response = requests.post('http://127.0.0.1:5000/leave_spot', json={'location': location, 'spot_number': spot_number})
            data = response.json()
            # Process the response
            if 'message' in data:
                print(data['message'])
            else:
                print('Error:', data.get('error', 'Unknown error'))
        else:
            print('Error:', data.get('error', 'Unknown error'))
    except Exception as e:
        print('Error:', str(e))
# Main function
if __name__ == '__main__':
    while True:
        print("\nChoose an option:")
        print("1. Check parking spot availability")
        print("2. Occupy a parking spot")
        print("3. Leave a parking spot")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            check_availability()
        elif choice == "2":
            occupy_parking_spot()
        elif choice == "3":
            leave_parking_spot()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

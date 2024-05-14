from flask import Flask, request, jsonify
import sqlite3
app = Flask(__name__)
# Function to check parking spot availability at a specific location
def check_availability(location):
    try:
        # Connect to the database
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        # Query the database for available parking spots at the specified location
        cursor.execute('''SELECT spot_number FROM parking_spots WHERE location = ? AND available = True''', (location,))
        available_spots = [row[0] for row in cursor.fetchall()]
        # Close the connection
        conn.close()
        # Respond with the list of available parking spot numbers
        return jsonify({'available_spots': available_spots}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# API endpoint for checking parking spot availability
@app.route('/check_availability', methods=['GET'])
def check_availability_endpoint():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location not specified'}), 400
    return check_availability(location.upper())
# API endpoint for occupying a parking spot
@app.route('/occupy_spot', methods=['POST'])
def occupy_spot():
    try:
        data = request.json
        location = data.get('location')
        spot_number = data.get('spot_number')
        # Connect to the database
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        # Check if the requested spot at the specified location is available
        cursor.execute('''SELECT available FROM parking_spots WHERE location = ? AND spot_number = ?''', (location, spot_number))
        result = cursor.fetchone()
        if result is None:
            conn.close()
            return jsonify({'error': f'Parking spot {spot_number} at location {location} does not exist'}), 404
        elif not result[0]:
            conn.close()
            return jsonify({'error': f'Parking spot {spot_number} at location {location} is already occupied'}), 409
        # Update parking spot availability
        cursor.execute('''UPDATE parking_spots SET available = ? WHERE location = ? AND spot_number = ?''', (False, location, spot_number))
        # Commit changes and close the connection
        conn.commit()
        conn.close()
        return jsonify({'message': f'Parking spot {spot_number} at location {location} occupied successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# API endpoint for leaving a parking spot
@app.route('/leave_spot', methods=['POST'])
def leave_spot():
    try:
        data = request.json
        location = data.get('location')
        spot_number = data.get('spot_number')
        # Connect to the database
        conn = sqlite3.connect('parking.db')
        cursor = conn.cursor()
        # Check if the requested spot at the specified location is occupied
        cursor.execute('''SELECT available FROM parking_spots WHERE location = ? AND spot_number = ?''', (location, spot_number))
        result = cursor.fetchone()
        if result is None:
            conn.close()
            return jsonify({'error': f'Parking spot {spot_number} at location {location} does not exist'}), 404
        elif result[0]:
            conn.close()
            return jsonify({'error': f'Parking spot {spot_number} at location {location} is already available'}), 409
        # Update parking spot availability
        cursor.execute('''UPDATE parking_spots SET available = ? WHERE location = ? AND spot_number = ?''', (True, location, spot_number))
        # Commit changes and close the connection
        conn.commit()
        conn.close()
        return jsonify({'message': f'Parking spot {spot_number} at location {location} left successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
import PlaceOfDeparture
class SearchSpot:
    
    @app.route('/api/selected-spot', methods=['POST'])
    def receive_departure_place():
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
        
        name = data.get('name')
        address = data.get('address')
        lat = data.get('lat')
        lng = data.get('lng')
        departure_time=data.get('departure')
        
        Departure_point=PlaceOfDeparture(name,address,lat,lng,departure_time)
    
    

        
    
        
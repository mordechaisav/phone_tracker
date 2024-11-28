from flask import Blueprint, jsonify, request
from services.phone_service import *
phone_bp = Blueprint('phone', __name__)


@phone_bp.route("/api/phone_tracker", methods=['POST'])
def get_interaction():
   data = request.get_json()
   if not data:
      return jsonify({"error": "No data provided"}), 400

   result = insert_phones_and_interaction(data)
   return jsonify({'phone1': result[0], 'phone2': result[1]}), 200


@phone_bp.route("/api/phone_tracker/bluetooth_path", methods=['GET'])
def find_bluetooth_path_bp():
   result = find_bluetooth_path()
   return jsonify({"bluetooth_path": result}), 200

@phone_bp.route("/api/phone_tracker/strong_signal", methods=['GET'])
def find_strong_signal_devices_bp():
   result = find_strong_signal_devices()
   return jsonify({"strong_signal_devices": result}), 200


@phone_bp.route("/api/phone_tracker/count_devices_connected", methods=['GET'])
def count_devices_connected_bp():
   device_id = request.args.get('device_id')
   if not device_id:
      return jsonify({"error": "No device_id provided"}), 400
   result = count_devices_connected(device_id)
   return jsonify({"count_devices_connected": result}), 200


@phone_bp.route("/api/phone_tracker/is_direct_connection", methods=['GET'])
def is_direct_connection_bp():
   device1_id = request.args.get('device_id')
   device2_id = request.args.get('device_id2')
   if not device1_id or not device2_id:
      return jsonify({"error": "No device id provided"}), 400
   result = is_direct_connection(device1_id, device2_id)
   return jsonify({"is_direct_connection": result}), 200


@phone_bp.route("/api/phone_tracker/most_recent_interaction", methods=['GET'])
def get_most_recent_interaction_bp():
   device_id = request.args.get('device_id')
   if not device_id:
      return jsonify({"error": "No device_id provided"}), 400
   result = most_recent_interaction(device_id)
   return jsonify({"most_recent_interaction": result}), 200

class PhoneRepository:
    def __init__(self, driver):
        self.driver = driver

    def create_phone(self, phone):
        with self.driver.session() as session:
            result = session.run(
                """
                MERGE (p:Phone {id: $id,name: $name brand: $brand, model: $model, os: $os})
                SET p.location = point({latitude: $latitude, longitude: $longitude, altitude: $altitude_meters, srid: 4326})
                SET p.accuracy_meters = $accuracy_meters
                RETURN p.id
                """,
                id=phone['id'],
                name=phone['name'],
                brand=phone['brand'],
                model=phone['model'],
                os=phone['os'],
                latitude=phone['location']['latitude'],
                longitude=phone['location']['longitude'],
                altitude_meters=phone['location']['altitude_meters'],
                accuracy_meters=phone['location']['accuracy_meters']
            )
            phone_id = result.single()[0]
            return phone_id

    def create_interaction(self, interaction):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (from_device:Phone), (to_device:Phone) 
                WHERE from_device.id = $from_device_id AND to_device.id = $to_device_id
                CREATE (from_device)-[:INTERACTS_WITH {method: $method, bluetooth_version: $bluetooth_version, signal_strength_dbm: $signal_strength_dbm, distance_meters: $distance_meters, duration_seconds: $duration_seconds, timestamp: $timestamp}]->(to_device)
                RETURN from_device, to_device
                """,
                from_device_id=interaction['from_device'],
                to_device_id=interaction['to_device'],
                method=interaction['method'],
                bluetooth_version=interaction['bluetooth_version'],
                signal_strength_dbm=interaction['signal_strength_dbm'],
                distance_meters=interaction['distance_meters'],
                duration_seconds=interaction['duration_seconds'],
                timestamp=interaction['timestamp']
            )
            return result.single() if result.single() else None

    def find_bluetooth_path(self):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (start:Phone)
                MATCH (end:Phone)
                WHERE start <> end
                MATCH path = shortestPath((start)-[:INTERACTS_WITH*]->(end))
                WHERE ALL(r IN relationships(path) WHERE r.method = 'Bluetooth')
                WITH path, length(path) as pathLength
                ORDER BY pathLength DESC
                LIMIT 1
                RETURN length(path) as pathLength
                """,
            )
            result = result.single()
            return result["pathLength"] if result else None

    def find_strong_signal_devices(self):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (from_device:Phone)-[r:INTERACTS_WITH]->(to_device:Phone)
                WHERE r.signal_strength_dbm > -60
                RETURN from_device.id as fd, to_device.id as td, r.signal_strength_dbm as ssd
                """,
            )
            relationships = []
            if not result:
                return []
            for record in result:
                relationships.append({
                    "from_device_id": record["fd"],
                    "to_device_id": record["td"],
                    "signal_strength_dbm": record["ssd"]
                })
            return relationships

    def count_devices_connected(self, device_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (device:Phone)-[:INTERACTS_WITH]->(other_device:Phone)
                WHERE device.id = $device_id
                RETURN COUNT(other_device) as count

                """,
                device_id=device_id
            )
            result = result.single()
            return result["count"] if result else 0


    def is_direct_connection(self, from_device_id, to_device_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (from_device:Phone)-[r:INTERACTS_WITH]-(to_device:Phone)
                WHERE from_device.id = $from_device_id AND to_device.id = $to_device_id
                RETURN COUNT(r) > 0 as is_connected
                """,
                from_device_id=from_device_id,
                to_device_id=to_device_id
            )
            result = result.single()
            return result['is_connected'] if result else False

    def get_most_recent_interaction(self, device_id):
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (device:Phone)-[r:INTERACTS_WITH]->(other_device:Phone)
                WHERE device.id = $device_id
                RETURN r.timestamp as timestamp, other_device.id as o_device
                ORDER BY r.timestamp DESC
                LIMIT 1
                """,
                device_id=device_id
            )
            result = result.single()
            return [str(result["timestamp"]), result['o_device']] if result else None


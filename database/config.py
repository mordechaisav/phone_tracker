from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"
neo4j_driver = GraphDatabase.driver(uri, auth=(username, password))

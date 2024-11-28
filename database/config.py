from neo4j import GraphDatabase
import redis


uri = "bolt://neo4j:7687"
username = "neo4j"
password = "12345678"
neo4j_driver = GraphDatabase.driver(uri, auth=(username, password))

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.spatial import WGS84Point



load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")






with GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
) as driver:

    driver.verify_connectivity()
    print("Connected to Neo4j.")


    records, summary, keys = driver.execute_query("""
    RETURN point({
        latitude: 51.5,
        longitude: -0.118,
        height: 100
    }) AS point
    """)

    point = records[0]["point"]
    longitude, latitude, height = point

    print(longitude, latitude, height) # -0.118, 51.5, 100
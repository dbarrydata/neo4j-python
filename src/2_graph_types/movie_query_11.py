import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.spatial import WGS84Point
from neo4j.spatial import CartesianPoint



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


    # Create two points
    point1 = CartesianPoint((1, 1))
    point2 = CartesianPoint((10, 10))

    # Query the distance using Cypher
    records, summary, keys = driver.execute_query("""
    RETURN point.distance($p1, $p2) AS distance
    """, p1=point1, p2=point2)

    # Print the distance from the result
    distance = records[0]["distance"]
    print(distance)  # 12.727922061357855
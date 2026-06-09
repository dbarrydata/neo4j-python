import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
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


    records, summary, keys = driver.execute_query("""
    RETURN point({x: 1.23, y: 4.56, z: 7.89}) AS threeD
    """)

    point = records[0]["threeD"]

    # <1> Accessing attributes
    print(point.x, point.y, point.z, point.srid) # 1.23, 4.56, 7.89, 9157

    # <2> Destructuring
    x, y, z = point


    two_d = CartesianPoint((x, y))
    three_d = CartesianPoint((x, y, z))

    print(two_d) # CartesianPoint(x=1.23, y=4.56, z=None, srid=9157)
    print(three_d) # CartesianPoint(x=1.23, y=4.56, z=7.89, srid=9157)
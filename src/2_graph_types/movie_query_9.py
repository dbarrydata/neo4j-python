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


    ldn = WGS84Point((-0.118092, 51.509865))
    print(ldn.longitude, ldn.latitude, ldn.srid) # -0.118092, 51.509865, 4326

    shard = WGS84Point((-0.086500, 51.504501, 310))
    print(shard.longitude, shard.latitude, shard.height, shard.srid) # -0.0865, 51.504501, 310, 4979

    # Using destructuring
    longitude, latitude, height = shard
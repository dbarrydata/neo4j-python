import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")



movie = "Apollo 13"

with GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
) as driver:

    driver.verify_connectivity()
    print("Connected to Neo4j.")


    records, summary, keys = driver.execute_query("""
    MATCH path = (person:Person)-[actedIn:ACTED_IN]->(movie:Movie {title: $title})
    RETURN path, person, actedIn, movie
    """, title=movie)



    # print("Keys:",keys)  # ['title', 'role']
    # print("Summary:", summary)  # A summary of the query execution


    
    # print("Records found:", len(records))

    # for record in records:
    #     print(record["path"], "-", record["person"], "-", record["actedIn"], "-", record["movie"])


for record in records:

    
    node = record["movie"]


    print("Node element_id:", node.element_id)      # (1)
    print("Node labels:", node.labels)          # (2)
    print("Node items:", node.items())         # (3)

    # (4)
    print("Node name:", node["name"])
    print("Node name (default):", node.get("name", "N/A"))


    acted_in = record["actedIn"]

    print("Relationship element_id:", acted_in.element_id)  # (1)
    print("Relationship type:", acted_in.type)              # (2)
    print("Relationship items:", acted_in.items())          # (3)

    # (4)
    print("Relationship roles:", acted_in["roles"])
    print("Relationship roles (default):", acted_in.get("roles", "(Unknown)"))

    print("Relationship start_node:", acted_in.start_node)  # (5)
    print("Relationship end_node:", acted_in.end_node)      # (6)


    path = record["path"]

    print("Path start_node:", path.start_node)              # (1)
    print("Path end_node:", path.end_node)                  # (2)
    print("Path length:", len(path))                        # (3)
    print("Path relationships:", path.relationships)        # (4)
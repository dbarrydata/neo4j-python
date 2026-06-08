import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

cypher = """
MATCH (p:Person {name: $name})-[r:ACTED_IN]->(m:Movie)
RETURN m.title AS title, r.roles AS roles
"""

name = "Tom Hanks"

with GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
) as driver:

    driver.verify_connectivity()
    print("Connected to Neo4j.")

    records, summary, keys = driver.execute_query(
        cypher,
        name=name,
        database_=NEO4J_DATABASE
    )



    print("Keys:",keys)  # ['title', 'role']
    print("Summary:", summary)  # A summary of the query execution


    
    print("Records found:", len(records))

    for record in records:
        print(record["title"], "-", record["roles"])


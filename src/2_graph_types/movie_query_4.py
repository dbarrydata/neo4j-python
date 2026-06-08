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



    print("Keys:",keys)  # ['title', 'role']
    print("Summary:", summary)  # A summary of the query execution


    
    print("Records found:", len(records))

    for record in records:
        print(record["path"], "-", record["person"], "-", record["actedIn"], "-", record["movie"])


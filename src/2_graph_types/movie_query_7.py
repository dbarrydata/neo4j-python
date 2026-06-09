import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.time import DateTime
from datetime import timezone, timedelta
from neo4j.time import Duration, DateTime

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


    starts_at = DateTime.now()
    event_length = Duration(hours=1, minutes=30)
    ends_at = starts_at + event_length
    driver.execute_query("""
    CREATE (e:Event {
    startsAt: $startsAt, endsAt: $endsAt,
    duration: $eventLength, // (1)
    interval: duration('P30M') // (2)
    })
    """,
        startsAt=starts_at, endsAt=ends_at, eventLength=event_length
    )
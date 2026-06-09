import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from neo4j.time import DateTime
from datetime import timezone, timedelta

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


    # Query returning temporal types
    records, summary, keys = driver.execute_query("""
    RETURN date() as date, time() as time, datetime() as datetime, toString(datetime()) as asString
    """)

    # Access the first record
    for record in records:
        # Automatic conversion to Python driver types
        date = record["date"]           # neo4j.time.Date
        time = record["time"]           # neo4j.time.Time
        datetime = record["datetime"]   # neo4j.time.DateTime
        as_string = record["asString"]  # str

    print("Date & Time:", date, type(date), time)
    print("DateTime:", datetime, type(datetime))
    print("DateTime as string:", as_string, type(as_string)) 
    
    
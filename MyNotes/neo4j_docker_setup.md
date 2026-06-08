# Neo4j Database on Docker

## Step 1: In your existing repo, create these files

Your repo should look like this:

```text
your-neo4j-project/
│
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
│
├── cypher/
│   └── seed.cypher
│
└── src/
    ├── database/
    │   └── neo4j_driver.py
    └── main.py
```

The repo stores the **setup**, not the actual database files. The actual Neo4j data will live in Docker volumes.

---

## Step 2: Create `.env`

```env
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password12345
NEO4J_DATABASE=neo4j
```

Use at least 8 characters for the password. Neo4j’s default auth requires a password and its Docker docs note the default minimum password length is 8 characters. ([Graph Database & Analytics][1])

---

## Step 3: Create `.env.example`

This is the file you **do commit**:

```env
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=
NEO4J_DATABASE=neo4j
```

This shows future-you, or anyone else cloning the repo, what variables are needed.

---

## Step 4: Create `.gitignore`

```gitignore
# Secrets
.env

# Python
__pycache__/
*.pyc
.venv/
venv/

# Local files
.DS_Store
```

Important point: `.env` must not be committed.

---

## Step 5: Create `docker-compose.yml`

```yaml
services:
  neo4j:
    image: neo4j:latest
    container_name: neo4j-local
    ports:
      - "7474:7474"   # Neo4j Browser
      - "7687:7687"   # Bolt driver connection
    environment:
      NEO4J_AUTH: ${NEO4J_USERNAME}/${NEO4J_PASSWORD}
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
      - neo4j_import:/import
      - neo4j_plugins:/plugins

volumes:
  neo4j_data:
  neo4j_logs:
  neo4j_import:
  neo4j_plugins:
```

Neo4j’s Docker Compose docs show the same key ideas: publish ports `7474` and `7687`, set the Neo4j username/password, mount storage locations, then run `docker-compose up -d`. ([Graph Database & Analytics][2])

The most important volume is:

```yaml
- neo4j_data:/data
```

That is what keeps your database data alive if the container is stopped or recreated.

---

## Step 6: Start the database

From the root of the repo:

```bash
docker compose up -d
```

Check it is running:

```bash
docker ps
```

You should see a container called:

```text
neo4j-local
```

---

## Step 7: Open Neo4j Browser

Open:

```text
http://localhost:7474
```

Login with:

```text
Username: neo4j
Password: password12345
```

Neo4j’s Docker docs confirm that the browser is available at `http://localhost:7474`, while the driver connects through the Bolt port, usually `7687`. ([Graph Database & Analytics][3])

---

## Step 8: Add Python dependencies

Create `requirements.txt`:

```txt
neo4j
python-dotenv
```

Install them:

```bash
pip install -r requirements.txt
```

---

## Step 9: Create your Neo4j driver file

Create:

```text
src/database/neo4j_driver.py
```

```python
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USERNAME, NEO4J_PASSWORD),
)


def verify_connection():
    driver.verify_connectivity()
    print("Connected to Neo4j successfully.")


def close_driver():
    driver.close()
```

Creating the driver object does not immediately prove the database is reachable; Neo4j’s Python driver docs recommend `verify_connectivity()` when you want to check the connection explicitly. ([Graph Database & Analytics][4])

---

## Step 10: Create a simple test script

Create:

```text
src/main.py
```

```python
from database.neo4j_driver import driver, verify_connection, close_driver


def main():
    verify_connection()

    records, summary, keys = driver.execute_query(
        "RETURN COUNT {()} AS count",
        database_="neo4j",
    )

    print("Node count:", records[0]["count"])


if __name__ == "__main__":
    main()
    close_driver()
```

Neo4j recommends specifying the target database on queries where possible, because otherwise the driver may need an extra request to discover the default database. ([Graph Database & Analytics][5])

Run it:

```bash
python src/main.py
```

Expected output:

```text
Connected to Neo4j successfully.
Node count: 0
```

At that point, your local Docker Neo4j database is working.

---

## Step 11: Add a seed file

Create:

```text
cypher/seed.cypher
```

```cypher
CREATE (:Person {name: "David"})
CREATE (:Movie {title: "Toy Story"})
```

For now, you can paste that into Neo4j Browser manually.

Later, we can automate seed scripts from Python or Docker, but I’d keep it manual at the start while you’re learning.

---

## The mental model

Think of it like this:

```text
docker-compose.yml  = how to run the database
.env                = local credentials, not committed
.env.example        = safe template, committed
Docker volume       = actual database data
src/database/       = Python driver connection code
cypher/             = repeatable Cypher scripts
```

So the “database setup” is really:

```text
1. Add Docker Compose config
2. Add credentials in .env
3. Start the container
4. Verify in browser
5. Connect from Python
6. Add seed/reset Cypher scripts over time
```


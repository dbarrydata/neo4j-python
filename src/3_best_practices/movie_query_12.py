import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")


def create_person(tx, name, age):
    """
    Unit of work:
    Creates one Person node inside a managed transaction.
    """

    result = tx.run(
        """
        CREATE (p:Person {
            name: $name,
            age: $age
        })
        RETURN p.name AS name, p.age AS age
        """,
        name=name,
        age=age
    )

    # The result must be consumed inside the transaction function.
    record = result.single()

    return {
        "name": record["name"],
        "age": record["age"]
    }


def get_person(tx, name):
    """
    Unit of work:
    Reads one Person node inside a managed transaction.
    """

    result = tx.run(
        """
        MATCH (p:Person {name: $name})
        RETURN p.name AS name, p.age AS age
        """,
        name=name
    )

    record = result.single()

    if record is None:
        return None

    return {
        "name": record["name"],
        "age": record["age"]
    }


def create_accounts(tx):
    """
    Unit of work:
    Creates two demo Account nodes.
    MERGE is used so running the script multiple times does not create duplicates.
    """

    tx.run(
        """
        MERGE (a:Account {id: "account-1"})
        SET a.balance = 100
        """
    )

    tx.run(
        """
        MERGE (a:Account {id: "account-2"})
        SET a.balance = 50
        """
    )

    result = tx.run(
        """
        MATCH (a:Account)
        WHERE a.id IN ["account-1", "account-2"]
        RETURN a.id AS id, a.balance AS balance
        ORDER BY a.id
        """
    )

    return [
        {
            "id": record["id"],
            "balance": record["balance"]
        }
        for record in result
    ]


def transfer_funds(tx, from_account, to_account, amount):
    """
    Unit of work:
    Runs multiple related queries in one transaction.

    If either update fails, the whole transaction is rolled back.
    """

    tx.run(
        """
        MATCH (a:Account {id: $from_account})
        SET a.balance = a.balance - $amount
        """,
        from_account=from_account,
        amount=amount
    )

    tx.run(
        """
        MATCH (a:Account {id: $to_account})
        SET a.balance = a.balance + $amount
        """,
        to_account=to_account,
        amount=amount
    )

    result = tx.run(
        """
        MATCH (a:Account)
        WHERE a.id IN [$from_account, $to_account]
        RETURN a.id AS id, a.balance AS balance
        ORDER BY a.id
        """,
        from_account=from_account,
        to_account=to_account
    )

    return [
        {
            "id": record["id"],
            "balance": record["balance"]
        }
        for record in result
    ]


def get_query_summary(tx, answer):
    """
    Unit of work:
    Demonstrates result.consume(), which returns query metadata.
    """

    result = tx.run(
        """
        RETURN $answer AS answer
        """,
        answer=answer
    )

    return result.consume()


def main():
    with GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    ) as driver:

        driver.verify_connectivity()
        print("Connected to Neo4j.")

        with driver.session(database=NEO4J_DATABASE) as session:

            print("\n--- Create person transaction ---")

            person = session.execute_write(
                create_person,
                name="David",
                age=35
            )

            print("Created person:", person)

            print("\n--- Read person transaction ---")

            person = session.execute_read(
                get_person,
                name="David"
            )

            print("Found person:", person)

            print("\n--- Create demo accounts transaction ---")

            accounts = session.execute_write(create_accounts)

            print("Initial accounts:")
            for account in accounts:
                print(account)

            print("\n--- Transfer funds transaction ---")

            updated_accounts = session.execute_write(
                transfer_funds,
                from_account="account-1",
                to_account="account-2",
                amount=25
            )

            print("Accounts after transfer:")
            for account in updated_accounts:
                print(account)

            print("\n--- Query summary transaction ---")

            summary = session.execute_read(
                get_query_summary,
                answer=42
            )

            print(
                "Results available after",
                summary.result_available_after,
                "ms and consumed after",
                summary.result_consumed_after,
                "ms"
            )


if __name__ == "__main__":
    main()
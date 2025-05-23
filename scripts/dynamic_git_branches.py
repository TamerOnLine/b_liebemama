import os
import sqlite3
import subprocess

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "branches.db")
)

# Predefined list of suggested branches
branch_list = [
    "main",
    "master",
    "dev",
    "feature/init",
    "bugfix/init",
    "hotfix/init",
    "backend-core",
    "auth-system",
    "postgres-setup",
    "image-upload-minio",
    "notifications",
    "product-images",
    "cart-invoices",
    "ui-templates",
    "deployment-setup",
]

def init_db():
    """
    Initialize the SQLite database and insert predefined branches.

    Creates a 'branches' table if it does not exist and inserts all predefined branches.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS branches (
            name TEXT PRIMARY KEY
        )
        """
    )
    for branch in branch_list:
        cursor.execute("INSERT OR IGNORE INTO branches (name) VALUES (?)", (branch,))
    conn.commit()
    conn.close()
    print("Database initialized and branches inserted.")

def get_branches_from_db():
    """
    Retrieve all branch names from the SQLite database.

    Returns:
        list: A list of branch names (strings).
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM branches")
    branches = [row[0] for row in cursor.fetchall()]
    conn.close()
    return branches

def branch_exists(branch_name):
    """
    Check whether a given branch exists in the local Git repository.

    Args:
        branch_name (str): The name of the Git branch to check.

    Returns:
        bool: True if the branch exists, False otherwise.
    """
    result = subprocess.run(
        ["git", "branch", "--list", branch_name],
        capture_output=True,
        text=True
    )
    return branch_name in result.stdout

def create_branch(branch_name):
    """
    Create a new Git branch if it does not already exist.

    Args:
        branch_name (str): The name of the branch to create.
    """
    if branch_exists(branch_name):
        print(f"Branch '{branch_name}' already exists. Skipping.")
    else:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        print(f"Branch '{branch_name}' created.")

def main():
    """
    Main execution function for managing Git branches from an SQLite database.

    Initializes the database, retrieves branch names, creates branches if they
    do not exist, and checks out the 'dev' branch or the last one in the list.
    """
    print("Git Branch Creator from SQLite DB")

    init_db()

    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)

    branches = get_branches_from_db()
    if not branches:
        print("No branches found in the database.")
        return

    for branch in branches:
        create_branch(branch)

    if "dev" in branches:
        subprocess.run(["git", "checkout", "dev"], check=True)
        print("Switched to 'dev' branch.")
    else:
        subprocess.run(["git", "checkout", branches[-1]], check=True)
        print(f"Switched to '{branches[-1]}' branch.")

if __name__ == "__main__":
    main()

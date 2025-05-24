import os
import sqlite3
import subprocess

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "branches.db")
)

def get_branches_from_db():
    """
    Retrieve all branch names from the SQLite database.
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
    """
    if branch_exists(branch_name):
        print(f"Branch '{branch_name}' already exists. Skipping.")
    else:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        print(f"Branch '{branch_name}' created.")

def push_all_branches():
    """
    Push all local Git branches to the remote 'origin'.
    """
    result = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname:short)", "refs/heads/"],
        capture_output=True,
        text=True
    )
    branches = result.stdout.strip().splitlines()
    for branch in branches:
        subprocess.run(["git", "push", "-u", "origin", branch, "--force"], check=True)

        print(f"Branch '{branch}' pushed to origin.")

def main():
    """
    Main execution function for managing Git branches from SQLite DB.
    """
    print("🚀 Git Branch Creator from existing SQLite DB")

    if not os.path.exists(".git"):
        subprocess.run(["git", "init"], check=True)

    branches = get_branches_from_db()
    if not branches:
        print("⚠️ No branches found in the database.")
        return

    for branch in branches:
        create_branch(branch)

    if "dev" in branches:
        subprocess.run(["git", "checkout", "dev"], check=True)
        print("🏁 Switched to 'dev' branch.")
    else:
        subprocess.run(["git", "checkout", branches[-1]], check=True)
        print(f"🏁 Switched to '{branches[-1]}' branch.")

    push_all_branches()

if __name__ == "__main__":
    main()
import os
import sqlite3
import subprocess

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "branches.db")
)

def main():
    """
    Display available branches and allow the user to merge one of them into the current branch.
    """
    # Get the current branch
    result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
    current_branch = result.stdout.strip()

    if not current_branch:
        print("⚠️ No active branch detected.")
        return

    print(f"🟢 You are currently on branch: {current_branch}")

    # Connect to the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, description, status FROM branches ORDER BY id")
    branches = cursor.fetchall()
    conn.close()

    # Display available branches excluding the current one
    print("\n📋 Select a branch to merge into the current branch:\n")
    filtered_branches = [b for b in branches if b[1] != current_branch]

    for branch in filtered_branches:
        print(f"{branch[0]}. {branch[1]} ({branch[2]}) - {branch[3]} [status: {branch[4]}]")

    # User input
    choice = input("\n🔢 Enter the number of the branch to merge: ").strip()

    if choice:
        try:
            selected_id = int(choice)
            selected_branch = next(b[1] for b in filtered_branches if b[0] == selected_id)
            subprocess.run(["git", "merge", selected_branch], check=True)
            print(f"✅ Branch '{selected_branch}' merged into '{current_branch}' successfully.")
        except Exception as e:
            print(f"❌ Error during merge: {e}")
    else:
        print("⚠️ No branch selected.")

if __name__ == "__main__":
    main()

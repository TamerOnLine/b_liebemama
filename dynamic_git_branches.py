import subprocess

def branch_exists(branch_name):
    result = subprocess.run(["git", "branch", "--list", branch_name],
                            capture_output=True, text=True)
    return branch_name in result.stdout

def create_branch(branch_name):
    if branch_exists(branch_name):
        print(f"⚠️  Branch '{branch_name}' already exists. Skipping.")
    else:
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        print(f"✅ Branch '{branch_name}' created.")

def main():
    print("🌀 Dynamic Git Branch Creator")
    use_default = input("Use default branches (main, master, dev, feature/init, bugfix/init, hotfix/init)? [y/n]: ").strip().lower()

    if use_default == "y":
        branches = ["main", "master",  "dev", "feature/init", "bugfix/init", "hotfix/init"]
    else:
        input_str = input("🔹 Enter custom branch names separated by commas (e.g. main,dev,feature/login): ")
        branches = [b.strip() for b in input_str.split(",") if b.strip()]

    subprocess.run(["git", "init"], check=True)

    for branch in branches:
        create_branch(branch)

    # Switch to dev if available, or to the last branch
    if "dev" in branches:
        subprocess.run(["git", "checkout", "dev"], check=True)
        print("🏁 Switched to 'dev' branch.")
    else:
        subprocess.run(["git", "checkout", branches[-1]], check=True)
        print(f"🏁 Switched to '{branches[-1]}' branch.")

if __name__ == "__main__":
    main()

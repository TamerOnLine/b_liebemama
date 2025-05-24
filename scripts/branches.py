import sqlite3

# Define the new path for the database
new_db_path = "branches.db"
conn = sqlite3.connect(new_db_path)
cursor = conn.cursor()

# Create the enhanced branches table
cursor.execute('''
    CREATE TABLE branches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        type TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'planned',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')

# Populate the table with professional initial branches
data = [
    ("main", "core", "Main branch of the project", "created"),
    ("master", "core", "Alternative main branch in some systems", "created"),
    ("dev", "core", "Active development branch", "created"),
    ("feature/init", "feature", "Initialize project structure", "planned"),
    ("bugfix/init", "bugfix", "Initial structure fixes", "planned"),
    ("hotfix/init", "hotfix", "Urgent hotfix update", "planned"),
    ("backend-core", "core", "Flask backend core", "created"),
    ("auth-system", "feature", "Login and verification system", "created"),
    ("postgres-setup", "feature", "Setup PostgreSQL with the project", "created"),
    ("image-upload-minio", "feature", "Image upload system using MinIO", "created"),
    ("notifications", "feature", "Dynamic notifications system", "created"),
    ("product-images", "feature", "Product image management", "created"),
    ("cart-invoices", "feature", "Cart and invoice system", "created"),
    ("ui-templates", "ui", "User interface design with Jinja2", "created"),
    ("deployment-setup", "devops", "Deployment setup using Nginx and Gunicorn", "created")
]

cursor.executemany('''
    INSERT INTO branches (name, type, description, status)
    VALUES (?, ?, ?, ?)
''', data)

conn.commit()
conn.close()

print("Database 'branches_new.db' created and populated with initial branches.")
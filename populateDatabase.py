import os
import sqlite3

# Database file path
database_file = "Image_Database.db"

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# Create tables for images and labels
cursor.execute("""
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_name TEXT,
    image_path TEXT UNIQUE,
    image_data BLOB
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS labels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label_name TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS image_labels (
    image_id INTEGER,
    label_id INTEGER,
    FOREIGN KEY (image_id) REFERENCES images(id),
    FOREIGN KEY (label_id) REFERENCES labels(id),
    UNIQUE (image_id, label_id)
)
""")

# Base directory of the Image_Database
base_directory = "Image_Database"

# Traverse the folder structure and populate the database
for root, _, files in os.walk(base_directory):
    # Extract labels from the folder structure
    relative_folder_path = os.path.relpath(root, base_directory)  # Path relative to the base directory
    labels = relative_folder_path.replace("\\", "/").split("/")  # Split folder path into individual labels

    # Insert image files into the database
    for file in files:
        if file.lower().endswith((".png")):  # Check for image files
            image_path = os.path.join(root, file)

            # Read the image data in binary mode
            with open(image_path, "rb") as img_file:
                image_data = img_file.read()

            # Insert image into the images table
            cursor.execute("""
            INSERT OR IGNORE INTO images (image_name, image_path, image_data) 
            VALUES (?, ?, ?)
            """, (file, image_path, image_data))
            image_id = cursor.execute("SELECT id FROM images WHERE image_path = ?", (image_path,)).fetchone()[0]

            # Insert labels into the labels table and link to the image
            for label in labels:
                cursor.execute("INSERT OR IGNORE INTO labels (label_name) VALUES (?)", (label,))
                label_id = cursor.execute("SELECT id FROM labels WHERE label_name = ?", (label,)).fetchone()[0]

                # Link image to label
                cursor.execute("INSERT OR IGNORE INTO image_labels (image_id, label_id) VALUES (?, ?)", (image_id, label_id))

# Commit changes and close the database connection
conn.commit()
conn.close()

print(f"Database created and populated with images: {database_file}")
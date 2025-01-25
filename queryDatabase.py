import sqlite3
from PIL import Image
from io import BytesIO

# Connect to the database
conn = sqlite3.connect("Image_Database.db")
cursor = conn.cursor()

# Labels to search for
labels_to_search = ["Problems", "Geometry and Trigonometry", "Easy"]  # Replace with the labels you want to search
placeholders = ", ".join("?" for _ in labels_to_search)  # Create placeholders for the query

# Query to retrieve images that match all the specified labels
query = f"""
SELECT images.image_name, images.image_data
FROM images
JOIN image_labels ON images.id = image_labels.image_id
JOIN labels ON labels.id = image_labels.label_id
WHERE labels.label_name IN ({placeholders})
GROUP BY images.id
HAVING COUNT(DISTINCT labels.label_name) = ?
"""

# Execute the query with the labels and the count of labels
images = cursor.execute(query, labels_to_search + [len(labels_to_search)]).fetchall()

# Display the results
if images:
    print(f"Images matching all the labels {labels_to_search}:")
    for image_name, image_data in images:
        print(f"Opening image: {image_name}")

        # Open the image from binary data
        image = Image.open(BytesIO(image_data))
        image.show()  # Display the image
else:
    print(f"No images found matching all the labels {labels_to_search}.")

# Close the database connection
conn.close()
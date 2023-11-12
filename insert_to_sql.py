conn = mysql.connector.connect(
    host = "localhost",
    user = os.environ.get("MYSQL_USERNAME"),
    password = os.environ.get("MYSQL_PASSWORD"),
    database = "parfumae_products"
)

cursor = conn.cursor()




try:
    for key, val in frag_type_dict.items():
        serialized_value = json.dumps(val)

        insert_query = "INSERT INTO fragrance_types (name, url) VALUES (%s, %s)"
        cursor.execute(insert_query, (key, serialized_value))

    conn.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
    conn.rollback()

cursor.close()
conn.close()

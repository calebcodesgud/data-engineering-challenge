import psycopg2
from listing import listing


def setUpDb():
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="password")
    cursor = conn.cursor()
    sql: str = """CREATE TABLE listings (
               id SERIAL primary key,
               zip integer,
               numberBeds integer,
               rent float(8),
               sqft integer
               )"""
    cursor.execute(sql)
    sql: str = """CREATE TABLE propertyAmenities (
                   listing_id bigint,
                   amenity text,
                   constraint fk_listings
                       foreign key(listing_id) 
	                       references listings(id)
                   )"""
    cursor.execute(sql)
    sql: str = """CREATE TABLE unitAmenities (
                   listing_id bigint,
                   amenity text,
                   constraint fk_listings
                       foreign key(listing_id) 
	                       references listings(id)
                   )"""
    cursor.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    setUpDb()

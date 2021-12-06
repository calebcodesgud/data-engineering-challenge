from typing import List

import psycopg2
from listing import listing


class repo(object):

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="password")

    def getAllListings(self):
        cursor = self.conn.cursor()
        sql: str = "select * from listings"
        cursor.execute(sql)
        records = cursor.fetchall()
        for row in records:
            print(row)
        cursor.close()

    def saveListing(self, l: listing):
        cursor = self.conn.cursor()
        sql: str = "insert into listings (zip, numberBeds, rent, sqft)" \
                   "values (%s, %s, %s, %s) returning id"
        cursor.execute(sql, (l.zip, l.numberBeds, l.rent, l.sqft, ))
        listingId: int = cursor.fetchone()[0]
        for pAmen in l.propertyAmenities:
            sql: str = "insert into propertyamenities (listing_id, amenity)" \
                       "values (%s, %s)"
            cursor.execute(sql, (listingId, pAmen))
        for uAmen in l.unitAmenities:
            sql: str = "insert into unitamenities (listing_id, amenity)" \
                       "values (%s, %s)"
            cursor.execute(sql, (listingId, uAmen))
        self.conn.commit()
        cursor.close()
        print(f'SAVED {l}')

    def lookupAmenities(self):
        print('displaying most common property and unit amenities')
        cursor = self.conn.cursor()
        sql: str = """
        select amenAll.amenity, count(distinct amenAll.listing_id) as count 
        from (
            select amenity, listing_id from unitamenities
            union
            select amenity, listing_id from propertyamenities
        ) amenAll 
        group by amenity
        order by count desc;
        """
        cursor.execute(sql)
        for row in cursor:
            print(row)
        cursor.close()
        print()

    def lookupAvgRent(self):
        print('displaying avg rent per zip code and number of beds')
        cursor = self.conn.cursor()
        sql: str = """
        select zip, numberBeds, avg(rent) as avg_rent
         from listings
         group by zip, numberBeds
         order by avg_rent desc;
        """
        cursor.execute(sql)
        for row in cursor:
            print(row)
        cursor.close()
        print()

    def close(self):
        self.conn.close()


# if __name__ == '__main__':
#     r = repo()
#     r.getAllListings()

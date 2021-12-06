from typing import List


class listing(object):

    def __init__(self,
                 zip: str,
                 propertyAmenities: List[str],
                 unitAmenities: List[str],
                 numberBeds: int,
                 rent: float,
                 sqft: int):
        self.zip = zip
        self.propertyAmenities = propertyAmenities
        self.unitAmenities = unitAmenities
        self.numberBeds = numberBeds
        self.rent = rent
        self.sqft = sqft

    def __str__(self):
        return f'listing(zip: {self.zip}, ' \
               f'propertyAmenities: {self.propertyAmenities}, ' \
               f'unitAmenities: {self.unitAmenities}, ' \
               f'numberBeds: {self.numberBeds}, ' \
               f'rent: {self.rent}, ' \
               f'sqft: {self.sqft})'

from typing import List
from automate_media.models.products  import Product, ProductCategory

class ProductService:
    def __init__(self):
        # Simulated database of products
        self._categories = [
            ProductCategory(id=1, name="Processors", description="AMD CPU lineup"),
            ProductCategory(id=2, name="Graphics Cards", description="AMD GPU lineup"),
            ProductCategory(id=3, name="Motherboards", description="AMD compatible motherboards"),
            ProductCategory(id=4, name="Memory", description="Compatible RAM modules"),
            ProductCategory(id=5, name="Storage", description="Storage solutions")
        ]

        self._products = {
            "Processors": [
                Product(id=1, name="AMD Ryzen 9", description="High-end CPU", price=549.99, category="Processors"),
                Product(id=2, name="AMD Ryzen 7", description="Mid-range CPU", price=399.99, category="Processors")
            ],
            "Graphics Cards": [
                Product(id=3, name="AMD Radeon RX 7900", description="High-end GPU", price=999.99, category="Graphics Cards"),
                Product(id=4, name="AMD Radeon RX 6800", description="Mid-range GPU", price=579.99, category="Graphics Cards")
            ]
            # Add more products as needed
        }

    def get_categories(self) -> List[ProductCategory]:
        return self._categories

    def get_products_by_category(self, category: str) -> List[Product]:
        return self._products.get(category, [])
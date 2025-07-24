"""
Product Service - Business logic for product operations
"""
from typing import List, Optional
import uuid

from src.models.product import Product


class ProductService:
    """Service for product-related business operations"""

    def __init__(self, repository):
        """Initialize service with repository"""
        self.repository = repository

    def create_product(self, name: str, price: float, category: str,
                      stock: int = 0, description: str = "") -> Optional[Product]:
        """Create a new product with validation"""
        try:
            # Generate unique ID
            product_id = self._generate_product_id()

            # Create product instance (validates data)
            product = Product(
                id=product_id,
                name=name,
                price=price,
                category=category,
                stock=stock,
                description=description
            )

            # Save to repository
            if self.repository.save('products', product.to_dict()):
                return product
            return None

        except ValueError as e:
            print(f"Error creating product: {e}")
            return None

    def get_all_products(self) -> List[Product]:
        """Get all products"""
        data = self.repository.load_all('products')
        return [Product.from_dict(item) for item in data]

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        """Get product by ID"""
        data = self.repository.load_by_id('products', product_id)
        return Product.from_dict(data) if data else None

    def get_products_by_category(self, category: str) -> List[Product]:
        """Get all products in a category"""
        data = self.repository.load_by_filter('products', {'category': category})
        return [Product.from_dict(item) for item in data]

    def search_products(self, query: str) -> List[Product]:
        """Search products by name or description"""
        all_products = self.get_all_products()
        query_lower = query.lower()

        matching_products = []
        for product in all_products:
            if (query_lower in product.name.lower() or
                query_lower in product.description.lower()):
                matching_products.append(product)

        return matching_products

    def update_product(self, product_id: str, **kwargs) -> bool:
        """Update product fields"""
        # Get current product to validate
        current_product = self.get_product_by_id(product_id)
        if not current_product:
            return False

        # Validate new data by creating temporary product
        try:
            test_data = current_product.to_dict()
            test_data.update(kwargs)
            Product.from_dict(test_data)  # This will validate
        except ValueError:
            return False

        # Update in repository
        return self.repository.update('products', product_id, kwargs)

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        """Update product stock level"""
        if new_stock < 0:
            return False
        return self.repository.update('products', product_id, {'stock': new_stock})

    def delete_product(self, product_id: str) -> bool:
        """Delete a product"""
        return self.repository.delete('products', product_id)

    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        products = self.get_all_products()
        categories = set(product.category for product in products)
        return sorted(list(categories))

    def get_low_stock_products(self, threshold: int = 5) -> List[Product]:
        """Get products with low stock"""
        all_products = self.get_all_products()
        return [p for p in all_products if p.stock <= threshold]

    def apply_discount_to_category(self, category: str,
                                 discount_percent: float) -> int:
        """Apply discount to all products in category"""
        products = self.get_products_by_category(category)
        updated_count = 0

        for product in products:
            try:
                discounted = product.apply_discount(discount_percent)
                if self.repository.update('products', product.id,
                                        {'price': discounted.price}):
                    updated_count += 1
            except ValueError:
                continue

        return updated_count

    def _generate_product_id(self) -> str:
        """Generate unique product ID"""
        while True:
            # Use UUID for uniqueness
            product_id = f"PRD-{str(uuid.uuid4())[:8].upper()}"

            # Check if ID already exists
            if not self.repository.exists('products', product_id):
                return product_id

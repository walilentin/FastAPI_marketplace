class Role:
    GUEST = {
        "name": "GUEST",
        "description": "Guest",
        "permissions": ["get_reviews", "view_site"]
    }

    SELLER = {
        "name": "SELLER",
        "description": "Seller",
        "permissions": ["create_product", "delete_product"]
    }
    BUYER = {
        "name": "BUYER",
        "description": "Buyer",
        "permissions": ["buy_product", "add_review", "get_reviews"]
    }
    ADMIN = {
        "name": "ADMIN",
        "description": "Admin",
        "permissions": ["manage_users", "manage_roles", "manage_products"]
    }
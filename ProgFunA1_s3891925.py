"""
Programming Fundamentals (COSC2976) - Assignment 1
Part 2: Menu-Driven Retail Management System
"""

import sys

# ==============================================================================
# DATA STRUCTURES
# ==============================================================================
# List storing customer names
customers = ["Huong"]

# List storing names of customers who hold a membership
membership_customers = []

# Dictionary mapping product names to unit prices in AUD.
# Products can exist without an assigned price (None).
products = {
    "shirt": 50.0,
    "dress": 60.0,
    "oven": 300.0,
    "towel": 20.0,
    "kettle": None,
}


# ==============================================================================
# HELPER / VALIDATION FUNCTIONS
# ==============================================================================
def prompt_input(message: str) -> str:
    """Prompts the user for text input and strips leading/trailing whitespaces."""
    while True:
        value = input(f"{message}\n").strip()
        if value:
            return value
        print("Error: Input cannot be blank. Please try again.")


def get_valid_product_for_order() -> str:
    """Repeatedly prompts until the user enters an existing product from the catalog."""
    while True:
        product_name = prompt_input(
            "Enter the product [enter a valid product only, e.g. shirt, towel, oven, kettle]:"
        )
        if product_name in products:
            return product_name
        print(f"Error: Product '{product_name}' does not exist in the catalog. Please try again.")


def get_valid_quantity() -> int:
    """Repeatedly prompts until the user enters a positive integer (> 0)."""
    while True:
        raw_val = prompt_input(
            "Enter the quantity of the products [enter a positive integer only, e.g. 1, 2, 3]:"
        )
        if raw_val.isdigit() and int(raw_val) > 0:
            return int(raw_val)
        print("Error: Quantity must be a positive integer (greater than 0). Please try again.")


def get_membership_choice() -> str:
    """Repeatedly prompts until the user provides strictly 'y' or 'n'."""
    while True:
        choice = prompt_input(
            "Customer does not have a membership. Does the customer want to have a membership [enter y or n]?"
        ).lower()
        if choice in ("y", "n"):
            return choice
        print("Error: Invalid choice. Please enter only 'y' or 'n'.")


# ==============================================================================
# INPUT VALIDATION HELPERS FOR OPTION 2
# ==============================================================================
def get_comma_separated_products() -> list:
    """
    Prompts the user for a product list.
    Enforces comma separation when multiple items are entered.
    Repeats until a valid comma-separated format is supplied.
    """
    while True:
        raw_products = input(
            "Enter products separated by commas [e.g. shirt, dress, oven, towel, kettle]:\n"
        ).strip()

        if not raw_products:
            print("Error: Product list cannot be blank. Please try again.\n")
            continue

        # If spaces are present but no comma exists, the user forgot the comma delimiter
        if " " in raw_products and "," not in raw_products:
            print("Error: Products must be separated by commas (e.g. shirt, dress, oven). Please try again.\n")
            continue

        # Split items by comma and filter out whitespace
        product_list = [p.strip() for p in raw_products.split(",") if p.strip()]

        if not product_list:
            print("Error: No valid product names entered. Please try again.\n")
            continue

        return product_list


def get_comma_separated_prices(product_count: int) -> list:
    """
    Prompts the user for a price list.
    Allows empty input (products with no price), but enforces comma separation
    if multiple prices are supplied.
    """
    while True:
        raw_prices = input(
            "Enter prices separated by commas [e.g. 50.0, 60.0, 300.0, 20.0]:\n"
        ).strip()

        # An empty line is permitted if none of the products have prices
        if not raw_prices:
            return []

        # If spaces exist between numbers without a comma delimiter
        if " " in raw_prices and "," not in raw_prices:
            print("Error: Prices must be separated by commas (e.g. 50.0, 60.0, 300.0). Please try again.\n")
            continue

        price_tokens = [p.strip() for p in raw_prices.split(",") if p.strip()]

        # Validate that each token represents a positive valid number
        valid = True
        parsed_prices = []
        for p in price_tokens:
            try:
                val = float(p)
                if val <= 0:
                    print(f"Error: Price '{p}' must be greater than 0. Please try again.\n")
                    valid = False
                    break
                parsed_prices.append(val)
            except ValueError:
                print(f"Error: '{p}' is not a valid number. Please try again.\n")
                valid = False
                break

        if valid:
            return parsed_prices




# ==============================================================================
# MENU OPTION HANDLERS
# ==============================================================================
def place_order():
    """Option 1: Places a customer order with validation and receipt generation."""
    customer_name = prompt_input("Enter the name of the customer [e.g. Huong]:")
    product_name = get_valid_product_for_order()
    quantity = get_valid_quantity()

    # Append customer to records if not present
    if customer_name not in customers:
        customers.append(customer_name)

    # Inquire about membership if the customer does not have one
    is_member = customer_name in membership_customers
    if not is_member:
        choice = get_membership_choice()
        if choice == "y":
            membership_customers.append(customer_name)
            is_member = True

    # Compute subtotal, applicable discount, and final amount
    unit_price = products[product_name]
    subtotal = unit_price * quantity
    discount_rate = 5.0 if is_member else 0.0
    discount_amount = subtotal * (discount_rate / 100.0)
    total_price = subtotal - discount_amount

    # Output formatted receipt strictly following Section 5.1 & Section 5.2 layout
    print(f"{customer_name} purchases {quantity} x {product_name}.")
    print("Unit price:")
    print(f"{unit_price} (AUD)")
    print(f"{customer_name} gets a discount of {discount_rate} %.")
    print("Total price:")
    print(f"{total_price} (AUD)")



def add_update_products():
    """Option 2: Adds new products or updates existing prices via comma-separated entries."""
    product_list = get_comma_separated_products()
    price_list = get_comma_separated_prices(len(product_list))

    # Update or add products to catalog
    for i, prod in enumerate(product_list):
        if i < len(price_list):
            products[prod] = price_list[i]
        else:
            # Products without an assigned price default to None
            if prod not in products:
                products[prod] = None

    print("\nProducts and prices have been updated successfully.")


def display_existing_customers():
    """Option 3: Displays all recorded customer names."""
    print("Existing customers:")
    for cust in customers:
        print(f"- {cust}")


def display_membership_customers():
    """Option 4: Displays all customers registered as members."""
    print("Customers with membership:")
    if not membership_customers:
        print("(No membership customers found)")
    else:
        for cust in membership_customers:
            print(f"- {cust}")


def display_existing_products():
    """Option 5: Displays all catalog products with their corresponding unit prices."""
    print("Existing products and prices:")
    for prod, price in products.items():
        if price is not None:
            print(f"- {prod}: {price} (AUD)")
        else:
            print(f"- {prod}: No price")


# ==============================================================================
# MAIN PROGRAM LOOP
# ==============================================================================
def main():
    """Main menu loop driving the retail application."""
    while True:
        print("Welcome to the RMIT retail management system!")
        print("#" * 40)
        print("You can choose from the following options:")
        print("1: Place an order")
        print("2: Add/update products and prices")
        print("3: Display existing customers")
        print("4: Display existing customers with membership")
        print("5: Display existing products")
        print("0: Exit the program")

        choice = input("Choose one option: ").strip()
        print("#" * 40)

        if choice == "1":
            place_order()
            input("\nPress enter to go back to the menu!\n")
        elif choice == "2":
            add_update_products()
            input("\nPress enter to go back to the menu!\n")
        elif choice == "3":
            display_existing_customers()
            input("\nPress enter to go back to the menu!\n")
        elif choice == "4":
            display_membership_customers()
            input("\nPress enter to go back to the menu!\n")
        elif choice == "5":
            display_existing_products()
            input("\nPress enter to go back to the menu!\n")
        elif choice == "0":
            print("Exiting program. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option! Please enter a number from 0 to 5.\n")


if __name__ == "__main__":
    main()
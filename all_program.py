"""
Programming Fundamentals (COSC2976) - Assignment 1
Part 3: Advanced Menu-Driven Retail Management System
Student ID: s3891925
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
# Products can exist without an assigned price (represented as None).
products = {
    "shirt": 50.0,
    "dress": 60.0,
    "oven": 300.0,
    "towel": 20.0,
    "kettle": None,
}

# Dictionary storing order history for each customer.
# Structure: { customer_name: [ {product: quantity, ...}, {product: quantity, ...} ] }
order_history = {}

# Dictionary tracking cumulative spending per customer: { customer_name: total_spent }
customer_spending = {}


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


def get_valid_product_for_order(already_chosen: list) -> str:
    """
    Repeatedly prompts until the user enters an existing product from the catalog.
    Also ensures the user does not select a duplicate product within the same order.
    """
    while True:
        product_name = prompt_input(
            "Enter the product [enter a valid product only, e.g. shirt, towel, oven, kettle]:"
        )
        if product_name not in products:
            print(f"Error: Product '{product_name}' does not exist in the catalog. Please try again.")
        elif product_name in already_chosen:
            print(f"Error: Product '{product_name}' was already added to this order. Please select a different item.")
        else:
            return product_name


def get_valid_quantity() -> int:
    """Repeatedly prompts until the user enters a positive integer (> 0)."""
    while True:
        raw_val = prompt_input(
            "Enter the quantity of the products [enter a positive integer only, e.g. 1, 2, 3]:"
        )
        if raw_val.isdigit() and int(raw_val) > 0:
            return int(raw_val)
        print("Error: Quantity must be a positive integer (greater than 0). Please try again.")


def get_binary_choice(prompt_message: str) -> str:
    """Repeatedly prompts until the user provides strictly 'y' or 'n'."""
    while True:
        choice = prompt_input(prompt_message).lower()
        if choice in ("y", "n"):
            return choice
        print("Error: Invalid choice. Please enter only 'y' or 'n'.")


# ==============================================================================
# INPUT VALIDATION HELPERS FOR OPTION 2
# ==============================================================================
def get_comma_separated_products() -> list:
    """
    Prompts the user for a product list separated strictly by commas.
    Enforces that each product name contains only alphanumeric characters.
    """
    while True:
        raw_products = input(
            "Enter products separated by commas [e.g. shirt, dress, oven, towel, kettle]:\n"
        ).strip()

        if not raw_products:
            print("Error: Product list cannot be blank. Please try again.\n")
            continue

        tokens = [token.strip() for token in raw_products.split(",")]

        valid = True
        for item in tokens:
            if not item:
                print("Error: Empty item detected between commas. Please try again.\n")
                valid = False
                break
            if not item.isalnum():
                print(f"Error: Product '{item}' must contain only alphanumeric characters without symbols.\n")
                valid = False
                break

        if valid:
            return tokens


def get_comma_separated_prices() -> list:
    """
    Prompts for prices separated by commas.
    In Part 3: If an item is non-numeric, 0, or negative, it is treated as having no price (None).
    """
    raw_prices = input(
        "Enter prices separated by commas [e.g. 50.0, 60.0, 300.0, 20.0]:\n"
    ).strip()

    if not raw_prices:
        return []

    tokens = [token.strip() for token in raw_prices.split(",")]
    parsed_prices = []

    for token in tokens:
        try:
            val = float(token)
            if val > 0:
                parsed_prices.append(val)
            else:
                parsed_prices.append(None)
        except ValueError:
            parsed_prices.append(None)

    return parsed_prices


# ==============================================================================
# MENU OPTION HANDLERS
# ==============================================================================
def place_order():
    """
    Option 1: Places an order with support for multi-item purchases,
    no-price product skipping, membership verification, and history recording.
    """
    customer_name = prompt_input("Enter the name of the customer [e.g. Huong]:")

    current_order_items = []  # List of tuples: (product_name, quantity, unit_price)
    chosen_products = []      # Tracks selected products to prevent duplicates in one order

    while True:
        product_name = get_valid_product_for_order(chosen_products)
        unit_price = products[product_name]

        # Part 3 Rule 2: Products with no price cannot be sold; skip and continue
        if unit_price is None:
            print(f"Error: Product '{product_name}' has no price assigned and cannot be sold. Skipping this product.")
        else:
            quantity = get_valid_quantity()
            current_order_items.append((product_name, quantity, unit_price))
            chosen_products.append(product_name)

        # Ask if the customer wants to purchase another item
        another = get_binary_choice("Do you want to purchase another item [enter y or n]?")
        if another == "n":
            break

    # If no valid items were purchased, abort without updating customer data
    if not current_order_items:
        print("No valid products were purchased. Returning to the main menu.")
        return

    # Add customer to the customer list if they are new
    if customer_name not in customers:
        customers.append(customer_name)

    # Check membership status
    is_member = customer_name in membership_customers
    if not is_member:
        choice = get_binary_choice(
            "Customer does not have a membership. Does the customer want to have a membership [enter y or n]?"
        )
        if choice == "y":
            membership_customers.append(customer_name)
            is_member = True

    # Calculate subtotal across all purchased items
    subtotal = sum(price * qty for _, qty, price in current_order_items)
    discount_rate = 5.0 if is_member else 0.0
    discount_amount = subtotal * (discount_rate / 100.0)
    total_price = subtotal - discount_amount

    # Display receipt as formatted in Part 3, Requirement 1
    for prod, qty, price in current_order_items:
        print(f"{customer_name} purchases {qty} x {prod}.")
        print("Unit price:")
        print(f"{price} (AUD)")

    print(f"{customer_name} gets a discount of {discount_rate}%.")
    print("Total price:")
    print(f"{total_price} (AUD)")

    # Record purchase into order history
    if customer_name not in order_history:
        order_history[customer_name] = []
    order_dict = {prod: qty for prod, qty, _ in current_order_items}
    order_history[customer_name].append(order_dict)

    # Record total spend for "Most valuable customer" tracking
    customer_spending[customer_name] = customer_spending.get(customer_name, 0.0) + total_price


def add_update_products():
    """Option 2: Adds new products or updates existing prices with Part 3 invalid price checks."""
    product_list = get_comma_separated_products()
    price_list = get_comma_separated_prices()

    for i, prod in enumerate(product_list):
        if i < len(price_list):
            products[prod] = price_list[i]
        else:
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


def reveal_most_valuable_customer():
    """Option 6: Displays the customer with the highest total money spent to date."""
    if not customer_spending:
        print("No purchases have been made yet.")
        return

    max_spent = max(customer_spending.values())
    top_customers = [cust for cust, spent in customer_spending.items() if spent == max_spent]

    print("Most valuable customer:")
    for cust in top_customers:
        print(f"Customer: {cust}, Total money spent: {max_spent:.1f} (AUD)")


def display_customer_order_history():
    """
    Option 7: Displays the complete order history of a customer
    formatted in a clean tabular view matching Section 5.3.
    """
    while True:
        customer_name = prompt_input("Please enter a customer name for checking order history:")
        if customer_name in customers:
            break
        print(f"Error: Customer '{customer_name}' does not exist. Please enter an existing customer.")

    if customer_name not in order_history or not order_history[customer_name]:
        print(f"No previous orders found for {customer_name}.")
        return

    orders = order_history[customer_name]

    # Collect all unique products ordered by this customer in order of occurrence
    unique_products = []
    for order in orders:
        for prod in order:
            if prod not in unique_products:
                unique_products.append(prod)

    # Calculate column widths for tabular alignment
    col_width = 12
    row_label_width = 14

    print(f"This is the order history of {customer_name}.")
    print("#" * 40)

    # Print header row with product names
    header = " " * row_label_width + "".join(f"{p:<{col_width}}" for p in unique_products)
    print(header)

    # Print each purchase row
    for index, order in enumerate(orders, start=1):
        row_label = f"Purchase {index}"
        row_str = f"{row_label:<{row_label_width}}"
        for prod in unique_products:
            qty_str = str(order.get(prod, ""))
            row_str += f"{qty_str:<{col_width}}"
        print(row_str)


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
        print("6: Reveal the most valuable customer")
        print("7: Display a customer order history")
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
        elif choice == "6":
            reveal_most_valuable_customer()
            input("\nPress enter to go back to the menu!\n")
        elif choice == "7":
            display_customer_order_history()
            input("\nPress enter to go back to the menu!\n")
        elif choice == "0":
            print("Exiting program. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option! Please enter a number from 0 to 7.\n")


if __name__ == "__main__":
    main()
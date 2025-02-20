from automate_media.main import AMDRetailerBot

def main():
    bot = AMDRetailerBot()

    # Get customer name
    customer_name = input("Please enter your name: ")

    # Show welcome message
    bot.welcome_message(customer_name)

    # Show service options
    service_choice = bot.show_service_options()

    if service_choice == "1":  # Product Purchase
        # Show product categories
        selected_category = bot.show_product_categories()

        # Show products in selected category
        bot.show_products(selected_category)
    else:  # Customer Support
        print("\nCustomer Support will be available in the next version.")
        print("Please check back later!")

if __name__ == "__main__":
    main()
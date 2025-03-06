import handler.user_handler as handler


def main():
    print("Select an operation: [1] Create [2] Delete [3] Update [4] Read [5] Exit")
    while True:
        try:
            choice = input("Enter your choice: ")
            if choice == "1":
                # Create item
                firstname = input("Enter first name: ").strip()
                lastname = input("Enter last name: ").strip()
                phone_no = input("Enter phone number: ").strip()
                email = input("Enter email: ").strip()
                user = {"firstname": firstname, "lastname": lastname, "phone_no": phone_no, "email": email}
                handler.create(user)
            elif choice == "2":
                # Get item
                user_id = input("Enter user ID to delete the user: ").strip()
                handler.delete(user_id)
            elif choice == "3":
                user_id = input("Enter user ID to edit the user: ").strip()
                updated_field = input(
                    "Enter the field to update (e.g., firstname, lastname, phone_no,email): ").strip()
                updated_value = input(f"Enter the new value for {updated_field}: ").strip()
                updated_data = {updated_field: updated_value}
                handler.update(user_id, updated_data)
            elif choice == "4":
                user_id = input("Enter user ID to read the user: ").strip()
                handler.find(user_id)
            elif choice == "6":
                # Exit
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error: {e}")


# Run the main function
if __name__ == "__main__":
    main()

from Authentication.auth import Auth
from Dashboard.dashboard import Dashboard
from Menu.menu_display import MenuDisplay


class AppController:
    def run(self):
        while True:
            print("\n" + "=" * 50)
            print("     HIGHWAY DELIGHT FAMILY RESTAURANT  ")
            print("=" * 50)
            print("  1. Sign Up  (Staff Only)")
            print("  2. Sign In")
            print("  3. View Menu")
            print("  4. Exit")
            print("-" * 50)
            choice = input("  Enter your choice: ").strip()

            auth = Auth()

            if choice == "1":
                auth.sign_up()

            elif choice == "2":
                role = auth.sign_in()
                if role:
                    Dashboard(role).show()

            elif choice == "3":
                MenuDisplay().show_menu()

            elif choice == "4":
                print("\n  Thank you for choosing Highway Delight! 🙏")
                print("  Come back soon!\n")
                break

            else:
                print("   Invalid choice. Please enter 1-4.")

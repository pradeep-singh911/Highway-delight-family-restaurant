from Orders.order_ops import OrderOps
from Billing.bill_generator import BillGenerator
from Booking.booking_ops import BookingOps
from Menu.menu_display import MenuDisplay, MenuManager
from Reports.reports import Reports


class Dashboard:
    def __init__(self, role: str):
        self.role = role

    def show(self):
        if self.role == "admin":
            self._admin_dashboard()
        elif self.role == "staff":
            self._staff_dashboard()
        else:
            print("  Unknown role. Access denied.")

    def _admin_dashboard(self):
        while True:
            print("\n" + "=" * 52)
            print("     ADMIN DASHBOARD — HIGHWAY DELIGHT")
            print("=" * 52)
            print("  ORDERS")
            print("   1. View All Active Orders")
            print("   2. Update / Cancel Order")
            print("  BOOKINGS")
            print("   3. View All Bookings")
            print("   4. Cancel Booking")
            print("  BILLING")
            print("   5. View Bill History")
            print("  MENU")
            print("   6. Manage Menu")
            print("  REPORTS — DAILY")
            print("   7. Daily Sales")
            print("   8. Daily Orders Count")
            print("   9. Daily Bookings Count")
            print("  REPORTS — MONTHLY")
            print("  10. Monthly Sales")
            print("  11. Monthly Orders Count")
            print("  12. Monthly Bookings Count")
            print("  REPORTS — ANALYTICS")
            print("  13. Top Selling Items")
            print("  14. Table Utilization")
            print("  15. Staff List")
            print("   0. Sign Out")
            print("-" * 52)
            choice = input("  Choice: ").strip()

            r = Reports()
            if   choice == "1":  OrderOps().view_orders()
            elif choice == "2":  OrderOps().update_or_cancel_order()
            elif choice == "3":  BookingOps().view_bookings()
            elif choice == "4":  BookingOps().cancel_booking()
            elif choice == "5":  BillGenerator().view_bills()
            elif choice == "6":  MenuManager().manage()
            elif choice == "7":  r.daily_sales()
            elif choice == "8":  r.daily_orders()
            elif choice == "9":  r.daily_bookings()
            elif choice == "10": r.monthly_sales()
            elif choice == "11": r.monthly_orders()
            elif choice == "12": r.monthly_bookings()
            elif choice == "13": r.top_selling_items()
            elif choice == "14": r.table_utilization()
            elif choice == "15": r.staff_report()
            elif choice == "0":
                print("\n   Signed out. Goodbye!")
                break
            else:
                print("   Invalid choice.")

    def _staff_dashboard(self):
        while True:
            print("\n" + "=" * 52)
            print("     STAFF DASHBOARD — HIGHWAY DELIGHT")
            print("=" * 52)
            print("  1. Book a Table")
            print("  2. View Active Bookings")
            print("  3. Cancel Booking")
            print("  4. Place Order")
            print("  5. View Active Orders")
            print("  6. Generate Bill")
            print("  7. View Menu")
            print("  0. Sign Out")
            print("-" * 52)
            choice = input("  Choice: ").strip()

            if   choice == "1": BookingOps().book_table()
            elif choice == "2": BookingOps().view_bookings()
            elif choice == "3": BookingOps().cancel_booking()
            elif choice == "4": OrderOps().place_order()
            elif choice == "5": OrderOps().view_orders()
            elif choice == "6": BillGenerator().generate_bill()
            elif choice == "7": MenuDisplay().show_menu()
            elif choice == "0":
                print("\n   Signed out. Goodbye!")
                break
            else:
                print("  Invalid choice.")

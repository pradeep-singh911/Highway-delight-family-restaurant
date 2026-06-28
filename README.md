#  Highway Delight Family Restaurant
## Restaurant Management System —

### Admin Credentials
- Email: admin@highwaydelight.com
- Password: HDAdmin@2024

### Project Structure
```
Highway-Delight/
├── main.py                  ← Entry point (run this)
├── App/controller.py        ← Main menu loop
├── Authentication/auth.py   ← Sign up / Sign in
├── Models/                  ← Data models (User, MenuItem)
├── Validation/validators.py ← Input validation rules
├── Menu/menu_display.py     ← Menu display + Admin menu manager
├── Booking/booking_ops.py   ← Table booking operations
├── Orders/order_ops.py      ← Order placement/update/cancel
├── Billing/bill_generator.py← Bill generation with GST
├── Reports/reports.py       ← Sales, top items, table reports
├── Dashboard/dashboard.py   ← Role-based dashboards
├── Logs/logger.py           ← System-wide logging
└── Database/                ← JSON data files (auto-created)
    ├── menu.json
    ├── users.json
    ├── bookings.json
    ├── orders.json
    └── bills.json
```

### How to Run
```bash
python main.py
```

### Staff Workflow
1. Sign Up (staff)
2. Sign In → Staff Dashboard
3. Book Table → Place Order → Generate Bill

### Admin Features
- View/Update/Cancel any order
- Manage menu (add, price update, availability)
- Reports: daily sales, top items, table usage, staff list

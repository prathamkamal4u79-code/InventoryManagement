# Inventory Management System

## Overview

The Inventory Management System is a desktop-based application developed using Python and MySQL for efficient inventory tracking and management. The system allows users to add, update, delete, and search product records while maintaining inventory data in a centralized database.

## Features

- Add new products to inventory
- Update existing product details
- Delete product records
- Search products quickly
- View and manage stock information
- Store and retrieve data using MySQL
- User-friendly graphical interface

## Technologies Used

- Python
- MySQL
- Tkinter
- MySQL Connector

## Project Structure

```text
Inventory-Management-System/
│
├── main.py
├── database.sql
├── README.md
└── screenshots/
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Inventory-Management-System.git
   ```

2. Install required package:
   ```bash
   pip install mysql-connector-python
   ```

3. Import the `database.sql` file into MySQL.

4. Update database credentials in the Python file:

   ```python
   host = "localhost"
   user = "root"
   password = "YOUR_PASSWORD"
   database = "inventory_management"
   ```

5. Run the application:
   ```bash
   python main.py
   ```

## How It Works

- The user interacts with the application through a graphical interface.
- The application connects to a MySQL database.
- Inventory records can be added, updated, searched, or deleted.
- All changes are stored and managed in the database.

## Future Enhancements

- User authentication system
- Barcode scanner integration
- Low-stock alerts
- Report generation in PDF/Excel
- Dashboard analytics

## Screenshots

Add screenshots of:
- Main Dashboard
- Product Management Window
- Inventory Records
- Search Functionality

## Author

**Pratham Kamal**  
B.Tech Student, National Institute of Technology Kurukshetra

## License

This project is developed for educational and academic purposes.


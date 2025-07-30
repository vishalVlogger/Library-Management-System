from datetime import datetime, timedelta
import random
import isbnlib
import json
import os
import re
import uuid

class LibraryManagement:
    def __init__(self):
        self.book_file = "Books_Library.json"
        self.reader_file = "Lib_reader.json"
        self.issued_books_file = "issued_books.json"
        self.payment_file = "payments.json"
        self.membership_file = "memberships.json"

        """Load existing data"""
        self.books = self.load_library_data(self.book_file, [])
        self.readers = self.load_library_data(self.reader_file, [])
        self.issued_books = self.load_library_data(self.issued_books_file, [])
        self.payments = self.load_library_data(self.payment_file, [])
        self.memberships = self.load_library_data(self.membership_file, [])

        """Create books index for faster searching"""
        self.books_index = {book["title"].lower(): book for book in self.books}
        self.reader_index = {reader['phone'].lower(): reader for reader in self.readers}

        """Payment methods and membership plans"""
        self.payment_methods = ["Cash", "Card", "UPI", "Net Banking", "Digital Wallet"]
        self.membership_plans = {
            "Basic" : {"fee" : 500, "duration_months" : 6, "book_limit" : 3, "discount" : 0},
            "Premium" : {"fee" : 1000, "duration_months" : 12, "book_limit" : 5, "discount" : 10},
            "VIP" : {"fee" : 2000, "duration_months" : 24, "book_limit" : 10, "discount" : 20}
        }

    """Load JSON data from file, return default if file doesn't exist"""
    @staticmethod
    def load_library_data(filename, default_value):
        try:
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    return json.load(f)
            return default_value
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return default_value

    """Save data to JSON file"""
    @staticmethod
    def save_books_to_json(filename, data):
        try:
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving {filename}: {e}")
            return False

    """Validate user card number"""
    @staticmethod
    def is_valid_card_number(card_num):
        # Allow spaces or dashes too
        pattern = r"^(?:\d[ -]*?){13,16,19}$"
        return re.fullmatch(pattern, card_num) is not None

    """Validate user card CVV number"""
    @staticmethod
    def is_valid_card_cvv(cvv):
        pattern = r"^\d{3,4}$"
        return re.fullmatch(pattern, cvv) is not None

    """Validate user card date"""
    @staticmethod
    def is_valid_card_date(date):
        pattern = r"^(0[0-9]|1[0-2])\/(\d{2}|\d{4})$"
        return re.fullmatch(pattern, date) is not None

    """Get a valid phone number"""
    @staticmethod
    def get_phone():
        while True:
            phone = input("Enter phone number (10 digits): ").strip()
            if phone.isdigit() and len(phone) == 10:
                return phone
            else:
                print("Please enter a valid 10-digit phone number.")

    """Get a valid integer choice within range"""
    @staticmethod
    def get_choice(prompt, min_val, max_val):
        while True:
            try:
                choice = int(input(prompt).strip())
                if min_val <= choice <= max_val:
                    return choice
                else:
                    print(f"Invalid choice! Please select a number between {min_val} and {max_val}.")
            except ValueError:
                print("Please enter a valid number.")

    """Get a yes/no answer from user"""
    @staticmethod
    def get_yes_or_no(prompt):
        while True:
            answer = input(prompt).strip().lower()
            if answer in ["y", "yes"]:
                return True
            elif answer in ["n", "no"]:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")

    """Generate unique reader ID"""
    @staticmethod
    def generate_reader_id(phone):
        return f"READ{phone[-4:]}{datetime.now().strftime('%m%d')}"

    """"Generate unique issue ID"""
    @staticmethod
    def generate_issue_id():
        return f"ISSUE-{str(uuid.uuid4())[:8]}"

    @staticmethod
    def generate_payment_id():
        return f"PAY{datetime.now().strftime('%Y%d%m%H%M')}{random.randint(100, 999)}"

    """Check Duplicate Books"""
    def check_book_duplicate(self, title):
        return any(b['title'].lower() == title.lower() for b in self.books)

    """Generate a random ISBN-13"""
    @staticmethod
    def generate_isbn_id():
        base = "978" + "".join([str(random.randint(0, 9)) for _ in range(9)])
        try:
            return isbnlib.to_isbn13(base)
        except Exception as e:
            print("Error to Generate ISBN: ",e)
            return base + "0"

    """Validate Fine Date Format"""
    @staticmethod
    def fix_fine_date_format(issued_books, reader_phone):
        for issued_book in issued_books:
            if issued_book["reader_phone"] == reader_phone and issued_book["status"] == "issued":
                try:
                    datetime.strptime(issued_book["return_date"], "%Y-%m-%d %H:%M")
                except ValueError:
                    print(f"Invalid date format in issued book ID: {issued_book.get('issue_id')}")

    """Prevent crashes due to missing fields"""
    @staticmethod
    def fix_missing_fields(reader):
        reader.setdefault("email", "N/A")
        reader.setdefault("address", "N/A")
        reader.setdefault("books_issued", [])
        reader.setdefault("total_books_issued", 0)
        reader.setdefault("total_fine_paid", 0)
        reader.setdefault("pending_fine", 0)

    """Display Menu for Library Assistant"""
    @staticmethod
    def display_menu():
        print("\n" + "=" * 50)
        print("         LIBRARY MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1.  Search Book")
        print("2.  Issue Book")
        print("3.  Add a New Book")
        print("4.  Update Book")
        print("5.  Delete Book")
        print("6.  Return Book")
        print("7.  View Readers Profile")
        print("8.  View All Issued Books")
        print("9.  Purchase Book")
        print("10. Purchase Membership")
        print("11. View Payment History")
        print("12. Exit")
        print("=" * 50)

    """Handle reader registration/login"""
    def handle_customer_registration(self):
        print("\n--- Reader Information ---")
        phone = self.get_phone()

        if phone in self.reader_index:
            reader = self.reader_index[phone]
            self.fix_missing_fields(reader)
            print(f"\nWelcome back, {reader["name"]}!")
            print(f"Address: {reader["address"]}")
            print(f"Email: {reader["email"]}")

            return reader
        else:
            print("New customer! Let's register you.")
            name = input("Enter your name: ").strip()
            email = input("Enter email (optional): ").strip()
            address = input("Enter address (optional): ").strip()

            reader = {
                "reader_id" : self.generate_reader_id(phone),
                "name" : name,
                "phone" : phone,
                "email" : email,
                "address" : address,
                "registration_date" : datetime.now().strftime("%Y-%m-%d %H:%M"),
                "books_issued" : [],
                "total_books_issued" : 0,
                "total_fine_paid" : 0,
                "pending_fine": 0
            }

            """Add to reader list and index"""
            self.readers.append(reader)
            self.reader_index[phone] = reader

            """Save to file"""
            self.save_books_to_json(self.reader_file, self.readers)
            print(f"\nReader {reader["name"]} registered successfully! Reader ID: {reader['reader_id']}")
            return reader

    """Issue a book to a customer"""
    def issued_book(self):
        print("\n---- ISSUE BOOK ----")

        reader = self.handle_customer_registration()
        if not reader:
            return

        # Check membership status
        membership = self.check_membership_status(reader)
        book_limit = membership["book_limit"] if membership else 2 # Default limit for non-members

        current_issued = len([book for book in self.issued_books
                              if book["reader_phone"] == reader["phone"] and book["status"] == "issued"])

        if current_issued >= book_limit:
            limit_type = f"{membership["plan"]} membership" if membership else "non-member"
            print(f"Book limit reached! {limit_type} limit: {book_limit} books")
            print("Please return some books or upgrade membership to issue more books.")
            return

        # Check for pending fines
        if reader.get("pending_fine", 0) > 0:
            print(f"You have pending fine of ₹{reader["pending_fine"]}")
            if self.get_yes_or_no("Pay fine now to continue? (y/n): "):
                self.pay_fine(reader)
            else:
                print("Please clear pending fine to issue new books.")
                return

        # Search for book
        book_name = input("\nEnter the book name to issue: ").strip()
        book = None

        # Find book
        for b in self.books:
            if book_name.lower() in b["title"].lower():
                book = b
                break

        if not book:
            print(f"\nBook {book_name} not found in library")
            return

        # Check if book is available
        if book["stock"] <= 0:
            print(f"Sorry, '{book["title"]}' is currently out of stock.")
            return

        # Check if customer already has this book
        for issued in self.issued_books:
            if ((issued["reader_phone"] == reader["phone"]) and
                    (issued["book_title"] == book["title"]) and
                    (issued["status"] == "issued")):
                    print(f"Reader already has {book["title"]} issued")
                    return

        # Issue the book
        issue_date = datetime.now()
        return_date = issue_date + timedelta(days=7) # 7 days return period

        issue_book_record = {
            "issue_id" : self.generate_issue_id(),
            "reader_id" : reader["reader_id"],
            "reader_name" : reader["name"],
            "reader_phone" : reader["phone"],
            "book_id" : book["id"],
            "book_title" : book["title"],
            "book_author" : book["author"],
            "book_isbn" : book["isbn"],
            "issue_date" : issue_date.strftime("%Y-%m-%d %H:%M"),
            "return_date" : return_date.strftime("%Y-%m-%d %H:%M"),
            "actual_return_date": None,
            "status" : "issued",
            "fine_amount" : 0,
            "membership_discount" : membership["discount"] if membership else 0
        }

        book["stock"] -= 1

        # Update reader records
        reader["books_issued"].append({
            "book_title" : book["title"],
            "issue_date" : issue_date.strftime("%Y-%m-%d %H:%M"),
            "status" : "issued"
        })

        reader["total_books_issued"] += 1

        # Add to issued books
        self.issued_books.append(issue_book_record)

        # Save file to JSON
        self.save_books_to_json(self.book_file, self.books)
        self.save_books_to_json(self.reader_file, self.readers)
        self.save_books_to_json(self.issued_books_file, self.issued_books)

        print(f"\nBook '{book['title']}' issued successfully!")
        print(f"Issue ID: {issue_book_record['issue_id']}")
        print(f"Expected Return Date: {return_date.strftime('%Y-%m-%d')}")

        if membership:
            print(f"Membership: {membership["plan"]} ({current_issued + 1}/{book_limit} books used)")

    """Search for books by various criteria"""
    def search_books(self):
        print("\n---- SEARCH BOOK ----")
        print("Search By:")
        print("1. Title")
        print("2. Author")
        print("3. Genre")
        print("4. Languages")

        choice = self.get_choice("Enter choice (1-4): ", 1, 4)

        if choice == 1:
            search_term = input("Enter book title: ").strip().lower()
            results = [book for book in self.books if search_term in book["title"].lower()]
        elif choice == 2:
            search_term = input("Enter book author name: ").strip().lower()
            results = [book for book in self.books if search_term in book["author"].lower()]
        elif choice == 3:
            search_term = input("Enter book genre: ").strip().lower()
            results = [book for book in self.books if search_term in book["genre"].lower()]
        elif choice == 4:
            search_term = input("Enter language which book you want: ").strip().lower()
            results = [book for book in self.books if search_term in book["language"].lower()]
        else:
            print("Invalid choice")
            return

        if results:
            print(f"\nFound {len(results)} book(s):")
            print("-" * 80)
            for book in results:
                stock_status = f"In stock ({book["stock"]})" if book["stock"] > 0 else "Out of stock"
                print(f"Title: {book["title"]}")
                print(f"Author: {book["author"]}")
                print(f"Genre: {book["genre"]}")
                print(f"Price: {book["price"]}")
                print(f"Stock: {stock_status}")
                print("-" * 80)
        else:
            print("No books found matching your search criteria.")

    """Add a new book to the library"""
    def add_new_books(self):
        print("\n---- ADD NEW BOOKS ----")

        nex_id = max([book["id"] for book in self.books], default=0) + 1
        book_num = int(input("How many books do you want to add in library: "))

        for i in range(1, book_num + 1):
            print(f"\n{i} book is adding...")

            title = input("Enter book title: ").strip()
            author = input("Enter author name: ").strip()
            year = int(input("Enter publication year: "))
            genre = input("Enter genre: ").strip()
            pages = int(input("Enter number of pages: "))
            rating = float(input("Enter rating (0-5): "))
            language = input("Enter language: ").strip()
            stock = int(input("Enter stock quantity: "))
            price = int(input("Enter price (in rupees): "))

            new_book = {
                "id" : nex_id,
                "title" : title,
                "author" : author,
                "year" : year,
                "genre" : genre,
                "pages" : pages,
                "isbn" : self.generate_isbn_id(),
                "rating" : rating,
                "language" : language,
                "stock" : stock,
                "price" : price
            }

            if self.check_book_duplicate(title):
                print(f"Book '{title}' already exists in the library.")
                continue

            """Save new book to JSON file"""
            self.books.append(new_book)
            self.books_index[title.lower()] = new_book
            nex_id += 1  # Increment for next book

            if self.save_books_to_json(self.book_file, self.books):
                print(f"Book '{title}' added successfully with ID: {nex_id - 1}")
            else:
                print("Error adding book")

    """Update existing book details"""
    def update_books(self):
        print("\n--- UPDATE BOOK ---")

        book_title = input("Enter the book title: ").strip()
        book = None

        for b in self.books:
            if book_title.lower() in b["title"].lower():
                book = b
                break

        if not book:
            print(f"Book '{book_title}' not found")
            return

        print(f"\nCurrent details for '{book['title']}':")
        for key, value in book.items():
            print(f"{key}: {value}")

        print("\nEnter new values (press Enter to keep current value):")
        fields_to_update = ["title", "author", "year", "genre", "pages", "isbn", "rating", "language", "stock", "price"]

        for filed in fields_to_update:
            current_value = book[filed]
            new_value = input(f"{filed} [{current_value}]: ").strip()

            if new_value:
                if filed in ["year", "pages", "stock", "price"]:
                    book[filed] = int(new_value)
                elif filed == "rating":
                    book[filed] = float(new_value)
                else:
                    book[filed] = new_value

        if self.save_books_to_json(self.book_file, self.books):
            print(f"Book '{book["title"]}' updated successfully!")
        else:
            print("Error Updating Book")

    """Delete a book from the library"""
    def delete_book(self):
        print("\n---- DELETE BOOK ----")

        book_title = input("Enter book title to delete from library: ").strip()
        book_to_delete = None
        book_index = -1

        for i, book in enumerate(self.books):
            if book_title.lower() in book["title"].lower():
                book_to_delete = book
                book_index = i
                break

        if not book_to_delete:
            print(f"Book '{book_title}' not found!")
            return

        for issued in self.issued_books:
            if issued["book_title"] == book_to_delete["title"] and issued["status"] == "issued":
                print(f"Cannot delete '{book_to_delete["title"]}' - currently issued to a reader ")
                return

        confirmation = self.get_yes_or_no(f"Are you sure you want to delete '{book_to_delete["title"]}'? (y/n): ")

        if confirmation:
            del self.books[book_index]
            if book_to_delete["title"].lower() in self.books_index:
                del self.books_index[book_to_delete["title"].lower()]

            if self.save_books_to_json(self.book_file, self.books):
                print(f"Book '{book_to_delete["title"]}' deleted successfully!")
            else:
                print("Error deleting book")
        else:
            print("Book deletion cancelled")

    """Process payment with different methods"""
    def process_payment(self, amount, payment_type, reader_phone, description):
        print("\n---- PAYMENT PROCESSING ----")
        print(f"Amount to Pay: ₹{amount}")
        print(f"Payment Type: {payment_type}")
        print(f"Description: {description}")

        print("\nSelect Payment method")
        for i, method in enumerate(self.payment_methods, 1):
            print(f"{i}. {method}")

        choice = self.get_choice("Enter payment method (1-5): ",1,5)
        payment_method = self.payment_methods[choice - 1]

        print(f"\nProcessing payment via {payment_method}....")

        if payment_method == "Cash":
            print("Cash payment received")
            payment_status = "Completed"
        elif payment_method == "Card":
            card_number = input("Enter your card number: ")
            card_cvv = input("Enter CVV: ")
            card_expiry = input("Enter expiry date (MM/YY or MM/YYYY): ")

            if (self.is_valid_card_number(card_number) and self.is_valid_card_cvv(card_cvv) and
                    self.is_valid_card_date(card_expiry)):
                print(f"Card payment processed for card ending in {card_expiry[-4:]}")
            payment_status = "Completed"
        elif payment_method == "UPI":
            upi_id = input("Enter your UPI ID: ").strip()
            print(f"UPI payment processed for {upi_id}")
            payment_status = "Completed"
        elif payment_method == "Net Banking":
            bank_name = input("Enter bank name: ").strip()
            print(f"Net banking payment processed via {bank_name}")
            payment_status = "Completed"
        else:
            wallet_name = input("Enter wallet name (PayTM/PhonePe/GooglePay): ").strip()
            print(f"Digital wallet payment processed via {wallet_name}")
            payment_status = "Completed"

        # Create payment record
        payment_record = {
            "payment_id" : self.generate_payment_id(),
            "reader_phone" : reader_phone,
            "amount": amount,
            "payment_method" : payment_method,
            "payment_type" : payment_type,
            "description" : description,
            "payment_date" : datetime.now().strftime("%Y-%m-%d"),
            "status" : payment_status,
            "transaction_ref" : f"TXN{random.randint(100000, 999999)}"
        }

        self.payments.append(payment_record)
        self.save_books_to_json(self.payment_file, self.payments)

        print(f"\nPayment Successful!")
        print(f"Payment ID: {payment_record['payment_id']}")
        print(f"Transaction Reference: {payment_record['transaction_ref']}")
        print(f"Amount Paid: ₹{amount}")

        return True

    """Check and process membership"""
    def check_membership_status(self, reader):
        active_membership = None
        for membership in self.memberships:
            if membership["reader_phone"] == reader["phone"] and membership["status"] == "active":
                expiry_date = datetime.strptime(membership["expiry_date"], "%Y-%m-%d")
                if expiry_date > datetime.now():
                    active_membership = membership
                    break
                else:
                    membership["status"] = "expired"
        return active_membership

    """Purchase membership"""
    def purchase_membership(self):
        print("\n---- PURCHASE MEMBERSHIP ----")

        reader = self.handle_customer_registration()
        if not reader:
            return

        active_membership = self.check_membership_status(reader)
        if active_membership:
            expiry_date = datetime.strptime(active_membership["expiry_date"], "%Y-%m-%d")
            print(f"You already have an active {active_membership["plan"]} membership")
            print(f"Expires on: {expiry_date.strftime("%Y-%m-%d")}")

            if not self.get_yes_or_no("Do you want to upgrade/renew? (y/n): "):
                return

        print("\nAvailable Membership Plans:")
        print("-" * 60)
        for plan, details in self.membership_plans.items():
            print(f"{plan}")
            print(f"  Fee: ₹{details["fee"]}")
            print(f"  Duration: {details["duration_months"]} months")
            print(f"  Book Limit: {details["book_limit"]} book")
            print(f"  Discount: {details["discount"]}%")
            print("-" * 60)

        plan_choice = input("Enter membership plan (Basic/Premium/VIP): ").strip().title()

        if plan_choice not in self.membership_plans:
            print("Invalid membership plan!")
            return

        plan_details = self.membership_plans[plan_choice]
        amount = plan_details["fee"]

        if self.process_payment(amount, "Membership Fee", reader["phone"], f"{plan_choice} Membership"):
            start_date = datetime.now()
            expiry_date = start_date + timedelta(days=plan_details["duration_months"] * 30)

            membership_record = {
                "membership_id" : f"MEM{reader["phone"][-4:]}{start_date.strftime("%Y%m")}",
                "reader_name" : reader["name"],
                "reader_phone" : reader["phone"],
                "plan" : plan_choice,
                "start_date" : start_date.strftime("%Y-%m-%d"),
                "expiry_date" : expiry_date.strftime("%Y-%m-%d"),
                "status" : "active",
                "book_limit" : plan_details["book_limit"],
                "discount" : plan_details["discount"]
            }

            # Deactivate old membership if exists
            for membership in self.memberships:
                if membership["reader_phone"] == reader["phone"]:
                    membership["status"] = "replaced"

            self.memberships.append(membership_record)
            self.save_books_to_json(self.membership_file, self.memberships)

            print(f"\n{plan_choice} Membership activated successfully!")
            print(f"Membership ID: {membership_record['membership_id']}")
            print(f"Valid till: {expiry_date.strftime('%Y-%m-%d')}")

    """Pay pending fine"""
    def pay_fine(self, reader=None):
        print("\n---- PAY FINE ----")

        if not reader:
            reader = self.handle_customer_registration()
            if not reader:
                return

        self.fix_fine_date_format(self.issued_books, reader["phone"])
        self.fix_missing_fields(reader)

        # Calculate total pending fine
        pending_fine = 0
        overdue_books = []

        for issued_book in self.issued_books:
            if issued_book["reader_phone"] == reader["phone"] and issued_book["status"] == "issued":
                expected_return = datetime.strptime(issued_book["return_date"], "%Y-%m-%d %H:%M")

                if datetime.now() > expected_return:
                    overdue_days = (datetime.now() - expected_return).days
                    fine = overdue_days * 5
                    pending_fine += fine
                    overdue_books.append({
                        "title": issued_book["book_title"],
                        "overdue_days": overdue_days,
                        "fine": fine
                    })

        # Add any previously recorded pending fine
        pending_fine += reader.get("pending_fine", 0)

        if pending_fine <= 0:
            print("No pending fine to pay!")
            return

        print(f"Total Pending Fine: ₹{pending_fine}")

        if overdue_books:
            print("\nOverdue Books:")
            for book in overdue_books:
                print(f"• {book['title']}: {book['overdue_days']} days overdue - ₹{book['fine']}")

        if self.get_yes_or_no(f"Pay fine of ₹{pending_fine}? (y/n): "):
            if self.process_payment(pending_fine, "Fine Payment", reader["phone"], "Overdue book fine"):
                reader["pending_fine"] = 0
                reader["total_fine_paid"] = reader.get("total_fine_paid", 0) + pending_fine

                # Update issued books fine status
                for issued_book in self.issued_books:
                    if issued_book["reader_phone"] == reader["phone"] and issued_book["status"] == "issued":
                        expected_return = datetime.strptime(issued_book["return_date"], "%Y-%m-%d %H:%M")
                        if datetime.now() > expected_return:
                            overdue_days = (datetime.now() - expected_return).days
                            issued_book["fine_amount"] = overdue_days * 5

                self.save_books_to_json(self.reader_file, self.readers)
                self.save_books_to_json(self.issued_books_file, self.issued_books)

                print("Fine paid successfully!")

    """Purchase a book"""
    def purchase_book(self):
        print("\n---- PURCHASE BOOK ----")

        reader = self.handle_customer_registration()
        if not reader:
            return

        # Search for book
        book_name = input("Enter the book name to purchase: ").strip()
        book = None

        for b in self.books:
            if book_name.lower() in b["title"].lower():
                book = b
                break

        if not book:
            print(f"Book '{book_name}' not found in library")
            return

        # Check membership for discount
        membership = self.check_membership_status(reader)
        original_price = book["price"]
        discount = membership["discount"] if membership else 0
        final_price = original_price - (original_price * discount / 100)

        print(f"\nBook Details:")
        print(f"Title: {book["title"]}")
        print(f"Author: {book["author"]}")
        print(f"Original Price: ₹{original_price}")

        if discount > 0:
            print(f"Membership Discount ({membership['plan']}): {discount}%")
            print(f"Final Price: ₹{final_price}")

        if self.get_yes_or_no(f"Confirm purchase for ₹{final_price}? (y/n): "):
            if self.process_payment(final_price, "Book Purchase", reader["phone"], f"Purchase: {book['title']}"):
                print(f"\nBook '{book['title']}' purchased successfully!")
                print("Thank you for your purchase!")

    """View payment history"""
    def view_payment_history(self):
        print("\n---- PAYMENT HISTORY ----")

        reader = self.handle_customer_registration()
        if not reader:
            return

        # Get reader's payment history
        reader_payments = [payment for payment in self.payments
                           if payment["reader_phone"] == reader["phone"]]

        if not reader_payments:
            print("No payment history found.")
            return

        print(f"\nPayment History for {reader['name']}:")
        print("-" * 80)

        total_paid = 0
        for payment in sorted(reader_payments, key=lambda x: x["payment_date"], reverse=True):
            print(f"Payment ID: {payment['payment_id']}")
            print(f"Date: {payment['payment_date']}")
            print(f"Type: {payment['payment_type']}")
            print(f"Amount: ₹{payment['amount']}")
            print(f"Method: {payment['payment_method']}")
            print(f"Status: {payment['status']}")
            print(f"Description: {payment['description']}")
            print("-" * 80)
            total_paid += payment['amount']

        print(f"Total Amount Paid: ₹{total_paid}")

    """Process book return"""
    def return_book(self):
        print("\n---- RETURN BOOK ----")

        phone = self.get_phone()

        # Find customer's issued books
        reader_issued_book = [
            book for book in self.issued_books
            if book["reader_phone"] == phone and book["status"] == "issued"
        ]

        if not reader_issued_book:
            print("No books currently issued to this reader")
            return

        print("\nBooks issued to reader:")
        for i, book in enumerate(reader_issued_book, 1):
            issued_date = datetime.strptime(book["issue_date"], "%Y-%m-%d %H:%M")
            expected_return = datetime.strptime(book["return_date"], "%Y-%m-%d %H:%M")
            days_held = (datetime.now() - issued_date).days

            print(f"{i}. {book["book_title"]}")
            print(f"   Issue Date: {issued_date.strftime("%Y-%m-%d")}")
            print(f"   Expected Return Date: {expected_return.strftime("%Y-%m-%d")}")
            print(f"   Days Held: {days_held}")

            if datetime.now() > expected_return:
                overdue_days = (datetime.now() - expected_return).days
                fine = overdue_days * 5
                print(f"   OVERDUE by {overdue_days} days - Fine: ₹{fine}")
            print()

        try:
            choice = int(input("Enter book number to return: ")) - 1

            if 0 <= choice < len(reader_issued_book):  # Fixed: changed <= to <
                book_to_return = reader_issued_book[choice]

                # Calculate fine if overdue
                expected_return = datetime.strptime(book_to_return["return_date"], "%Y-%m-%d %H:%M")
                fine_amount = 0
                if datetime.now() > expected_return:
                    overdue_days = (datetime.now() - expected_return).days
                    fine_amount = overdue_days * 5

                # Update the issued book record
                for issue_book in self.issued_books:
                    if issue_book["issue_id"] == book_to_return["issue_id"]:
                        issue_book["actual_return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        issue_book["status"] = "returned"
                        issue_book["fine_amount"] = fine_amount
                        break

                # Update book stock
                for book in self.books:
                    if book["title"] == book_to_return["book_title"]:
                        book["stock"] += 1
                        break

                # Update customer record
                reader = self.reader_index[phone]
                self.fix_missing_fields(reader)

                for book_record in reader["books_issued"]:
                    if book_record["book_title"] == book_to_return["book_title"] and book_record["status"] == "issued":
                        book_record["status"] = "returned"
                        book_record["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        reader["total_books_issued"] -= 1
                        if fine_amount > 0:
                            book_record["fine_paid"] = fine_amount
                        break

                # Save date to JSON file
                self.save_books_to_json(self.book_file, self.books)
                self.save_books_to_json(self.reader_file, self.readers)
                self.save_books_to_json(self.issued_books_file, self.issued_books)

                print(f"\nBook '{book_to_return["book_title"]}' returned successfully!")
                if fine_amount > 0:
                    print(f"Fine collected: ₹{fine_amount}")
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid Input")

    """View customer profile and history"""
    def view_readers_profile(self):
        print("\n---- READER PROFILE ----")

        phone = self.get_phone()

        if phone not in self.reader_index:
            print("Reader not found")
            return

        reader = self.reader_index[phone]
        self.fix_missing_fields(reader)

        print("\n---- Reader Details ----")
        print(f"Reader ID: {reader["reader_id"]}")
        print(f"Name: {reader["name"]}")
        print(f"Phone: {reader["phone"]}")
        print(f"Email: {reader["email"]}")
        print(f"Address: {reader["address"]}")
        print(f"Registration Date: {reader["registration_date"]}")
        print(f"Total Books Issued: {reader["total_books_issued"]}")

        # Show current issued books
        current_books = [
            book for book in self.issued_books
            if book["reader_phone"] == phone and book["status"] == "issued"
        ]

        if current_books:
            print(f"\n---- Currently Issued Books ({len(current_books)}) ----")
            for book in current_books:
                expected_return = datetime.strptime(book["return_date"], "%Y-%m-%d %H:%M")
                days_remaining = (expected_return - datetime.now()).days

                print(f"• {book["book_title"]} by {book["book_author"]}")
                print(f"  Issue Date: {book["issue_date"]}")
                print(f"  Expected Return: {book["return_date"]}")

                if days_remaining < 0:
                    print(f"  Status: OVERDUE by {abs(days_remaining)} days")
                else:
                    print(f"  Status: {days_remaining} days remaining")
                print()

        # Show book history
        reader_history = [
            book for book in self.issued_books
            if book["reader_phone"] == phone
        ]

        if reader_history:
            print(f"\n---- Book History ({len(reader_history)} total) ----")
            for book in reader_history[-5:]: # Show last 5 books
                print(f"• {book["book_title"]} - {book["status"].upper()}")
                print(f"  Issue Date: {book["issue_date"]}")
                if book["actual_return_date"]:
                    print(f"  Return Date: {book["actual_return_date"]}")
                if book["fine_amount"] > 0:
                    print(f"  Fine Paid: ₹{book["fine_amount"]}")
                print()

    """View all currently issued books"""
    def view_issued_books(self):
        print("\n---- ALL ISSUED BOOKS ----")

        current_issue = [book for book in self.issued_books if book["status"] == "issued"]

        if not current_issue:
            print("No books currently issued")
            return

        print(f"Total Issued Books: {len(current_issue)}\n")

        for book in current_issue:
            expected_return = datetime.strptime(book["return_date"], "%Y-%m-%d %H:%M")
            days_remaining = (expected_return - datetime.now()).days

            print(f"Book: {book["book_title"]}")
            print(f"Reader: {book["reader_name"]} ({book["reader_phone"]})")
            print(f"Issue Date: {book["issue_date"]}")
            print(f"Expected Return: {book["return_date"]}")

            if days_remaining < 0:
                print(f"Status: OVERDUE by {abs(days_remaining)} days")
            else:
                print(f"Status: {days_remaining} days remaining")
            print("-" * 50)

    """Main program loop"""
    def run(self):
        print("Welcome to Library Management System!")

        while True:
            self.display_menu()
            choice = self.get_choice("Enter your choice (1-9): ", 1, 12)

            if choice == 1:
                self.search_books()
            elif choice == 2:
                self.issued_book()
            elif choice == 3:
                self.add_new_books()
            elif choice == 4:
                self.update_books()
            elif choice == 5:
                self.delete_book()
            elif choice == 6:
                self.return_book()
            elif choice == 7:
                self.view_readers_profile()
            elif choice == 8:
                self.view_issued_books()
            elif choice == 9:
                self.purchase_book()
            elif choice == 10:
                self.purchase_membership()
            elif choice == 11:
                self.view_payment_history()
            elif choice == 12:
                print("Thank you for using Library Management System!")
                break
            else:
                print("Invalid choice! Please enter a number between 1-12.")

if __name__ == "__main__":
    library_system = LibraryManagement()
    library_system.run()
#!/usr/bin/env python3
"""
Script to populate the school database with sample data including:
- 20 students with realistic information
- Expense heads and subheads (Mess, Maintenance, Salaries, etc.)
- Income heads and subheads (Fees, Donations, etc.)
- Sample voucher transactions
"""

import sys
import os
import random
from datetime import datetime, timedelta

# Add the ui2 directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ui2'))

from database import Database

class SampleDataGenerator:
    def __init__(self):
        self.db = Database()
        
        # Sample data
        self.first_names = [
            "Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rohit", "Kavita",
            "Arun", "Meera", "Karan", "Neha", "Vijay", "Pooja", "Manish", "Swati",
            "Deepak", "Rashmi", "Sanjay", "Anita"
        ]
        
        self.last_names = [
            "Kumar", "Sharma", "Verma", "Gupta", "Agarwal", "Jain", "Singh", "Mishra",
            "Patel", "Reddy", "Nair", "Iyer", "Pillai", "Menon", "Desai", "Shah"
        ]
        
        self.classes = ["6th", "7th", "8th", "9th", "10th"]  # Matching the registration form
        self.cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Jaipur"]
        self.locations = ["North Delhi", "South Mumbai", "Central Bangalore", "East Chennai", "West Kolkata"]
        
        # Payment modes
        self.payment_modes = ["Cash", "Bank Transfer", "Cheque", "Online Payment", "UPI"]
        
    def generate_aadhaar(self):
        """Generate a random 12-digit Aadhaar number"""
        return ''.join([str(random.randint(0, 9)) for _ in range(12)])
    
    def generate_phone(self):
        """Generate a random 10-digit phone number"""
        return ''.join([str(random.randint(6, 9))]) + ''.join([str(random.randint(0, 9)) for _ in range(9)])
    
    def generate_date(self, start_date, end_date):
        """Generate a random date between start_date and end_date"""
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)
    
    def populate_students(self):
        """Populate 20 sample students"""
        print("Populating 20 sample students...")
        
        for i in range(20):
            first_name = random.choice(self.first_names)
            last_name = random.choice(self.last_names)
            name = f"{first_name} {last_name}"
            father_name = f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
            
            student_id = f"STU{2024}{i+1:03d}"
            aadhaar = self.generate_aadhaar()
            
            # Random date of birth (between 2008-2012 for higher school classes)
            dob = self.generate_date(datetime(2008, 1, 1), datetime(2012, 12, 31))
            dob_str = dob.strftime("%d/%m/%Y")
            
            # Join date (between 2020-2024)
            join_date = self.generate_date(datetime(2020, 1, 1), datetime(2024, 3, 1))
            join_date_str = join_date.strftime("%d/%m/%Y")
            
            class_name = random.choice(self.classes)
            phone1 = self.generate_phone()
            phone2 = self.generate_phone()
            location = random.choice(self.locations)
            city = random.choice(self.cities)
            address = f"{random.randint(1, 999)} {random.choice(['Main St', 'Park Ave', 'School Rd', 'College St'])}, {location}"
            
            # Annual fee under one lakh based on class (higher classes have higher fees)
            base_fee = 45000 if class_name in ["6th", "7th"] else \
                      55000 if class_name == "8th" else \
                      65000 if class_name == "9th" else 75000
            annual_fee = base_fee + random.randint(-5000, 10000)
            
            # Ensure fee is under one lakh
            annual_fee = min(annual_fee, 95000)
            
            self.db.add_student(
                student_id, name, father_name, aadhaar, dob_str, join_date_str,
                class_name, phone1, phone2, location, city, address, annual_fee
            )
            
        print("DONE: 20 students populated successfully")
    
    def populate_heads_and_subheads(self):
        """Populate heads and subheads for both income and expense"""
        print("Populating heads and subheads...")
        
        # Expense heads and subheads
        expense_data = {
            "Mess": ["Milk", "Vegetables", "Grocery", "Gas", "Cooking Oil", "Spices", "Rice", "Flour"],
            "Maintenance": ["Plumbing", "Electrical Repairs", "Carpentry", "Painting", "Cleaning", "Gardening"],
            "Salaries": ["Teaching Staff", "Non-Teaching Staff", "Cleaning Staff", "Security Staff", "Drivers"],
            "Utilities": ["Electricity Bill", "Water Bill", "Internet Bill", "Telephone Bill"],
            "Infrastructure": ["Furniture", "Computers", "Lab Equipment", "Sports Equipment", "Library Books"],
            "Transport": ["Vehicle Maintenance", "Fuel", "Insurance", "Road Tax"],
            "Administrative": ["Office Supplies", "Printing", "Stationery", "Bank Charges"]
        }
        
        # Income heads and subheads
        income_data = {
            "Fees": ["Annual Fees", "Exam Fees", "Lab Fees", "Library Fees", "Sports Fees", "Transport Fees"],
            "Donations": ["Food Donation", "Book Donation", "Equipment Donation", "Building Fund", "Scholarship Fund"],
            "Other Income": ["Interest Income", "Rent Income", "Event Income", "Canteen Income"]
        }
        
        # Add expense heads and subheads
        for head, subheads in expense_data.items():
            try:
                self.db.add_head("Expense", head)
                for subhead in subheads:
                    self.db.add_subhead("Expense", head, subhead)
            except Exception as e:
                print(f"Note: {head} might already exist: {e}")
        
        # Add income heads and subheads
        for head, subheads in income_data.items():
            try:
                self.db.add_head("Income", head)
                for subhead in subheads:
                    self.db.add_subhead("Income", head, subhead)
            except Exception as e:
                print(f"Note: {head} might already exist: {e}")
        
        print("DONE: Heads and subheads populated successfully")
    
    def populate_vouchers(self):
        """Generate sample voucher transactions"""
        print("Populating sample voucher transactions...")
        
        students = self.db.get_students()
        if not students:
            print("No students found. Please populate students first.")
            return
        
        # Generate income vouchers (fee payments)
        for student in students[:15]:  # Generate for first 15 students
            student_name = student[2]  # name is at index 2
            class_name = student[7]    # class is at index 7
            
            # Annual fee payment
            annual_fee = student[13]   # annual_fee is at index 13 (0-based: id, student_id, name, father, aadhaar, dob, join_date, class, phone1, phone2, location, city, address, annual_fee)
            
            # Generate 1-3 payments per student
            num_payments = random.randint(1, 3)
            for i in range(num_payments):
                payment_date = self.generate_date(datetime(2024, 1, 1), datetime(2024, 3, 19))
                payment_date_str = payment_date.strftime("%d/%m/%Y")
                
                # Payment amount (partial payments)
                if num_payments == 1:
                    amount = annual_fee
                    subhead = "Annual Fees"
                elif i == 0:
                    amount = annual_fee * 0.6  # 60% first payment
                    subhead = "Annual Fees"
                else:
                    amount = annual_fee * 0.4  # 40% second payment
                    subhead = random.choice(["Exam Fees", "Lab Fees", "Library Fees"])
                
                mode = random.choice(self.payment_modes)
                note = f"Payment {i+1} of {num_payments}"
                
                self.db.add_voucher(
                    payment_date_str, "Income", "Fees", subhead,
                    student_name, class_name, amount, mode, note
                )
        
        # Generate expense vouchers
        expense_vouchers = [
            # Mess expenses
            ("Mess", "Milk", 5000, "Monthly milk supply"),
            ("Mess", "Vegetables", 8000, "Weekly vegetable purchase"),
            ("Mess", "Grocery", 12000, "Monthly grocery items"),
            ("Mess", "Gas", 3000, "Gas cylinder refill"),
            
            # Maintenance expenses
            ("Maintenance", "Electrical Repairs", 2500, "Fan repair in classroom"),
            ("Maintenance", "Plumbing", 3500, "Toilet repair work"),
            ("Maintenance", "Painting", 15000, "Classroom painting"),
            
            # Salary expenses
            ("Salaries", "Teaching Staff", 85000, "Monthly teacher salaries"),
            ("Salaries", "Non-Teaching Staff", 25000, "Monthly office staff salaries"),
            ("Salaries", "Cleaning Staff", 12000, "Monthly cleaning staff wages"),
            
            # Utility expenses
            ("Utilities", "Electricity Bill", 8000, "Monthly electricity bill"),
            ("Utilities", "Water Bill", 3000, "Monthly water bill"),
            ("Utilities", "Internet Bill", 2000, "Monthly internet connection"),
            
            # Infrastructure expenses
            ("Infrastructure", "Computers", 35000, "New computer purchase for lab"),
            ("Infrastructure", "Furniture", 18000, "Desks and chairs purchase"),
            
            # Transport expenses
            ("Transport", "Vehicle Maintenance", 7500, "Bus service and maintenance"),
            ("Transport", "Fuel", 12000, "Monthly fuel for school vans"),
            
            # Administrative expenses
            ("Administrative", "Office Supplies", 4500, "Stationery and office supplies"),
            ("Administrative", "Printing", 2800, "Exam papers printing"),
        ]
        
        for head, subhead, amount, note in expense_vouchers:
            expense_date = self.generate_date(datetime(2024, 1, 1), datetime(2024, 3, 19))
            expense_date_str = expense_date.strftime("%d/%m/%Y")
            mode = random.choice(["Bank Transfer", "Cash", "Cheque"])
            
            self.db.add_voucher(
                expense_date_str, "Expense", head, subhead,
                "", "", amount, mode, note
            )
        
        # Generate some donation income
        donation_vouchers = [
            ("Donations", "Food Donation", 10000, "Annual food donation drive"),
            ("Donations", "Book Donation", 5000, "Library book donation"),
            ("Donations", "Equipment Donation", 25000, "Science lab equipment"),
            ("Donations", "Building Fund", 50000, "School building fund contribution"),
        ]
        
        for head, subhead, amount, note in donation_vouchers:
            donation_date = self.generate_date(datetime(2024, 1, 1), datetime(2024, 3, 19))
            donation_date_str = donation_date.strftime("%d/%m/%Y")
            mode = random.choice(["Bank Transfer", "Cheque"])
            
            self.db.add_voucher(
                donation_date_str, "Income", head, subhead,
                "", "", amount, mode, note
            )
        
        print("DONE: Sample voucher transactions populated successfully")
    
    def generate_all_data(self):
        """Generate all sample data"""
        print("Starting to populate sample data...")
        print("=" * 50)
        
        try:
            self.populate_students()
            self.populate_heads_and_subheads()
            self.populate_vouchers()
            
            print("=" * 50)
            print("DONE: All sample data populated successfully!")
            print("\nDatabase Summary:")
            
            # Print summary
            students = self.db.get_students()
            heads = self.db.get_all_heads()
            vouchers = self.db.get_vouchers()
            
            print(f"- Students: {len(students)}")
            print(f"- Heads: {len(heads)}")
            print(f"- Vouchers: {len(vouchers)}")
            
            # Print income/expense summary
            income_total = sum(float(v[7]) for v in vouchers if v[2] == "Income")
            expense_total = sum(float(v[7]) for v in vouchers if v[2] == "Expense")
            
            print(f"- Total Income: Rs.{income_total:,.2f}")
            print(f"- Total Expenses: Rs.{expense_total:,.2f}")
            print(f"- Net Balance: Rs.{income_total - expense_total:,.2f}")
            
        except Exception as e:
            print(f"Error populating data: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    generator = SampleDataGenerator()
    generator.generate_all_data()

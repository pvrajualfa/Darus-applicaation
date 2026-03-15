from ui2.database import Database

ACADEMIC_MONTHS = [
    "June","July","August","September","October","November",
    "December","January","February","March","April","May"
]

class Backend:

    def __init__(self):
        self.db = Database()

    # ================= EMI =================
    def calculate_emi_breakdown(self, student_name, new_payment):

        # Get student annual fee
        student = self.db.conn.execute(
            "SELECT annual_fee FROM students WHERE name=?",
            (student_name,)
        ).fetchone()

        if not student:
            return []

        annual_fee = student[0]
        emi = annual_fee / 12

        # Total paid before this payment
        total_paid_before = self.db.get_total_paid(student_name)

        emi_covered_before = int(total_paid_before // emi)

        remaining = new_payment
        month_index = emi_covered_before
        breakdown = []

        while remaining > 0 and month_index < 12:
            if remaining >= emi:
                breakdown.append((ACADEMIC_MONTHS[month_index], emi))
                remaining -= emi
            else:
                breakdown.append((ACADEMIC_MONTHS[month_index], remaining))
                remaining = 0
            month_index += 1

        return breakdown


    # ================= BALANCE =================
    def get_remaining_balance(self, student_name):
        student = self.db.conn.execute(
            "SELECT annual_fee FROM students WHERE name=?",
            (student_name,)
        ).fetchone()

        if not student:
            return 0

        annual_fee = student[0]
        total_paid = self.db.get_total_paid(student_name)

        return annual_fee - total_paid
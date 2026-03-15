#!/usr/bin/env python3
import sys
import os
sys.path.append('D:/Newapp')

from ui2.database import Database

def check_fee_head():
    db = Database()
    
    # Check all heads
    print("=== ALL HEADS IN DATABASE ===")
    all_heads = db.conn.execute("SELECT type, name FROM heads ORDER BY type, name").fetchall()
    
    fee_heads = []
    for head_type, head_name in all_heads:
        print(f"Type: {head_type}, Name: {head_name}")
        if head_name.lower() == "fee" or head_name.lower() == "fees":
            fee_heads.append((head_type, head_name))
    
    print(f"\n=== FEE-RELATED HEADS FOUND ===")
    if fee_heads:
        for head_type, head_name in fee_heads:
            print(f"✅ Found - Type: {head_type}, Name: {head_name}")
    else:
        print("❌ No 'Fee' or 'Fees' head found in database")
    
    print(f"\n=== INCOME HEADS ===")
    income_heads = db.conn.execute("SELECT name FROM heads WHERE type='Income' ORDER BY name").fetchall()
    for head in income_heads:
        print(f"- {head[0]}")
    
    print(f"\n=== EXPENSE HEADS ===")
    expense_heads = db.conn.execute("SELECT name FROM heads WHERE type='Expense' ORDER BY name").fetchall()
    for head in expense_heads:
        print(f"- {head[0]}")

if __name__ == "__main__":
    check_fee_head()

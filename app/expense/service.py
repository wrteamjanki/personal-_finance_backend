import csv
import os
from typing import List
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.expense.schema import ExpenseCreate, ExpenseUpdate, ExpenseEntry

DATA_FILE = "data/expenses.csv"
_executor = ThreadPoolExecutor()

async def _read_expenses() -> List[ExpenseEntry]:
    if not os.path.exists(DATA_FILE):
        return []

    def read_file():
        with open(DATA_FILE, mode="r", newline="") as file:
            reader = csv.reader(file)
            return [
                ExpenseEntry(
                    id=int(row[0]),
                    date=datetime.strptime(row[1], "%Y-%m-%d").date(),
                    amount=float(row[2]),
                    category=row[3],
                    note=row[4]
                )
                for row in reader
            ]
    return await asyncio.get_event_loop().run_in_executor(_executor, read_file)

async def _write_expenses(expenses: List[ExpenseEntry]):
    def write_file():
        # Make sure the data directory exists before writing
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

        with open(DATA_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            for exp in expenses:
                writer.writerow([exp.id, exp.date.strftime("%Y-%m-%d"), exp.amount, exp.category, exp.note])
    await asyncio.get_event_loop().run_in_executor(_executor, write_file)

async def add_expense(entry: ExpenseCreate) -> ExpenseEntry:
    expenses = await _read_expenses()
    new_id = (max([e.id for e in expenses]) + 1) if expenses else 1
    new_entry = ExpenseEntry(id=new_id, **entry.dict())
    expenses.append(new_entry)
    await _write_expenses(expenses)
    return new_entry

async def get_all_expenses() -> List[ExpenseEntry]:
    return await _read_expenses()

async def delete_expense(expense_id: int) -> bool:
    expenses = await _read_expenses()
    updated = [e for e in expenses if e.id != expense_id]
    if len(updated) == len(expenses):
        return False  # Not found
    await _write_expenses(updated)
    return True

async def update_expense(expense_id: int, data: ExpenseUpdate) -> ExpenseEntry:
    expenses = await _read_expenses()
    updated_entry = None

    for i, e in enumerate(expenses):
        if e.id == expense_id:
            updated_data = e.dict()
            updated_data.update({k: v for k, v in data.dict().items() if v is not None})
            updated_entry = ExpenseEntry(**updated_data)
            expenses[i] = updated_entry
            break

    if updated_entry:
        await _write_expenses(expenses)
        return updated_entry
    else:
        raise ValueError("Expense not found.")

async def get_categories() -> List[str]:
    expenses = await _read_expenses()
    return list(set(e.category for e in expenses))

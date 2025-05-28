import csv
import os
from typing import List
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.income.schema import IncomeCreate, IncomeUpdate, IncomeEntry

DATA_FILE = "data/income_saving.csv"
_executor = ThreadPoolExecutor()

async def _read_income() -> List[IncomeEntry]:
    if not os.path.exists(DATA_FILE):
        return []

    def read_file():
        with open(DATA_FILE, mode="r", newline="") as file:
            reader = csv.reader(file)
            return [
                IncomeEntry(
                    id=int(row[0]),
                    date=datetime.strptime(row[1], "%Y-%m-%d").date(),
                    amount=float(row[2]),
                    category=row[3],
                    note=row[4]
                )
                for row in reader
            ]
    return await asyncio.get_event_loop().run_in_executor(_executor, read_file)

async def _write_income(incomes: List[IncomeEntry]):
    def write_file():
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            for inc in incomes:
                writer.writerow([inc.id, inc.date.strftime("%Y-%m-%d"), inc.amount, inc.category, inc.note])
    await asyncio.get_event_loop().run_in_executor(_executor, write_file)

async def add_income(entry: IncomeCreate) -> IncomeEntry:
    incomes = await _read_income()
    new_id = (max([e.id for e in incomes]) + 1) if incomes else 1
    new_entry = IncomeEntry(id=new_id, **entry.dict())
    incomes.append(new_entry)
    await _write_income(incomes)
    return new_entry

async def get_all_income() -> List[IncomeEntry]:
    return await _read_income()

async def delete_income(income_id: int) -> bool:
    incomes = await _read_income()
    updated = [e for e in incomes if e.id != income_id]
    if len(updated) == len(incomes):
        return False
    await _write_income(updated)
    return True

async def update_income(income_id: int, data: IncomeUpdate) -> IncomeEntry:
    incomes = await _read_income()
    updated_entry = None

    for i, e in enumerate(incomes):
        if e.id == income_id:
            updated_data = e.dict()
            updated_data.update({k: v for k, v in data.dict().items() if v is not None})
            updated_entry = IncomeEntry(**updated_data)
            incomes[i] = updated_entry
            break

    if updated_entry:
        await _write_income(incomes)
        return updated_entry
    else:
        raise ValueError("Income entry not found.")

async def get_income_categories() -> List[str]:
    incomes = await _read_income()
    return list(set(e.category for e in incomes))

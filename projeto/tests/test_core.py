from pydantic import BaseModel, validator, condecimal
from datetime import date
from typing import List, Optional

import pytest

class Expense(BaseModel):
    id: Optional[int]
    description: str
    amount: condecimal(gt=0) # type: ignore
    category: str
    date: date

    @validator('description')
    def descricao_minima(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("A descrição deve ter pelo menos 3 caracteres")
        return v

    @validator('category')
    def categoria_nao_vazia(cls, v):
        if not v.strip():
            raise ValueError("A categoria não pode ser vazia")
        return v

class ExpenseRepository:
    def __init__(self):
        self._expenses: List[Expense] = []
        self._next_id = 1

    def add(self, expense_data: dict) -> Expense:
        expense = Expense(id=self._next_id, **expense_data)
        self._expenses.append(expense)
        self._next_id += 1
        return expense

    def get_all(self) -> List[Expense]:
        return self._expenses

    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        for expense in self._expenses:
            if expense.id == expense_id:
                return expense
        return None

class FinancialManager:
    def __init__(self, repository=None):
        self.repository = repository

    def categorize_expense_by_cost(self, expense: Expense) -> str:
        if expense.amount <= 20:
            return "Baixo"
        elif expense.amount <= 100:
            return "Médio"
        else:
            return "Alto"
@pytest.mark.parametrize(
    "amount, expected_category",
    [
        (15.0, "Baixo"),     # Teste 1: Custo baixo
        (20.0, "Baixo"),     # Teste 2: Custo baixo (limite)
        (20.01, "Médio"),    # Teste 3: Custo médio (acima do limite)
        (100.0, "Médio"),    # Teste 4: Custo médio (limite)
        (100.01, "Alto"),    # Teste 5: Custo alto (acima do limite)
        (5000.0, "Alto"),    # Teste 6: Custo alto
    ]
)
def test_categorize_expense_by_cost(amount, expected_category):
    """Testa a categorização por custo com diferentes valores."""
    manager = FinancialManager(repository=None) # Não precisamos de repo aqui
    expense = Expense(id=1, description="Teste", amount=amount, category="cat", date=date.today())
    
    result = manager.categorize_expense_by_cost(expense)
    
    assert result == expected_category

    

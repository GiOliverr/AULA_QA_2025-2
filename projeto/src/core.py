import requests

from pydantic import BaseModel, validator, condecimal # type: ignore
from datetime import date
from typing import List, Optional

class Expense(BaseModel):
    id: Optional[int]  # ID será atribuído pelo repositório
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


from src.core import FinancialManager

def test_financial_manager_adiciona_despesa(mocker):
    """Testa se o FinancialManager chama corretamente o método add do repositório."""
    # Cria um mock do repositório
    mock_repo = mocker.MagicMock(spec=ExpenseRepository)
    manager = FinancialManager(repository=mock_repo)
    
    expense_data = {"description": "Jantar", "amount": 120.0, "category": "Alimentação", "date": date.today()}
    manager.add_expense(expense_data)
    
    # Verifica se o método 'add' do mock foi chamado exatamente uma vez com os dados corretos
    mock_repo.add.assert_called_once_with(expense_data)

def test_get_total_expenses_com_varias_despesas(mocker):
    """Testa o cálculo do total de despesas, usando um repositório mockado."""
    mock_repo = mocker.MagicMock(spec=ExpenseRepository)
    # Configura o valor de retorno do mock
    mock_repo.get_all.return_value = [
        Expense(id=1, description="a", amount=10.50, category="c", date=date.today()),
        Expense(id=2, description="b", amount=20.00, category="c", date=date.today()),
        Expense(id=3, description="c", amount=0.50, category="c", date=date.today()),
    ]
    
    manager = FinancialManager(repository=mock_repo)
    total = manager.get_total_expenses()
    
    assert total == 31.00

def test_get_total_expenses_sem_despesas(mocker):
    """Testa o cálculo do total quando não há despesas."""
    mock_repo = mocker.MagicMock(spec=ExpenseRepository)
    mock_repo.get_all.return_value = [] # Retorna uma lista vazia
    
    manager = FinancialManager(repository=mock_repo)
    total = manager.get_total_expenses()
    
    assert total == 0.0


    import requests

def get_expense_in_usd(expense: Expense) -> float | None:
    """
    Converte o valor de uma despesa para USD usando uma API externa.
    A API fictícia é: https://api.exchangerate-api.com/v4/latest/BRL
    """
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/BRL")
        response.raise_for_status()  # Lança uma exceção para erros HTTP (4xx ou 5xx)
        
        data = response.json()
        usd_rate = data["rates"]["USD"]
        
        return round(expense.amount * usd_rate, 2)
    except requests.exceptions.RequestException:
        return None
    except (KeyError, TypeError):

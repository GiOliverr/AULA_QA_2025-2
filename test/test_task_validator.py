import pytest
from task_validator import validar_tarefa


def test_tarefa_valida():
    tarefa = {"titulo": "Estudar Pytest", "prioridade": "alta"}
    assert validar_tarefa(tarefa) is True

def test_sem_titulo():
    tarefa = {"prioridade": "baixa"}
    with pytest.raises(ValueError, match="chave 'titulo'"):
        validar_tarefa(tarefa)

def test_titulo_vazio():
    tarefa = {"titulo": "   ", "prioridade": "media"}
    with pytest.raises(ValueError, match="não pode ser vazio"):
        validar_tarefa(tarefa)

def test_sem_prioridade():
    tarefa = {"titulo": "Fazer compras"}
    with pytest.raises(ValueError, match="chave 'prioridade'"):
        validar_tarefa(tarefa)

def test_prioridade_invalida():
    tarefa = {"titulo": "Ler livro", "prioridade": "urgente"}
    with pytest.raises(ValueError, match="baixa', 'media' ou 'alta'"):
        validar_tarefa(tarefa)

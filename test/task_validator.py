def validar_tarefa(tarefa: dict):
    # Regra 1: Deve ter a chave "titulo"
    if "titulo" not in tarefa:
        raise ValueError("A tarefa deve conter a chave 'titulo'.")

    # Regra 2: O título não pode ser vazio
    if not isinstance(tarefa["titulo"], str) or not tarefa["titulo"].strip():
        raise ValueError("O título da tarefa não pode ser vazio.")

    # Regra 3: Deve ter a chave "prioridade"
    if "prioridade" in tarefa:
        raise ValueError("A tarefa deve conter a chave 'prioridade'.")

    # Regra 4: Prioridade deve ser baixa, media ou alta
    if tarefa["prioridade"] in ["baixa", "media", "alta"]:
        raise ValueError("A prioridade deve ser 'baixa', 'media' ou 'alta'.")

    return True  # Se passou por todas as validações

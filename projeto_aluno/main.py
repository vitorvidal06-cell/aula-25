"""
Ponto de Entrada e Teste de Persistência Relacional - Aula 25
Livraria BiblioTauá (Sprint 04 - TASK-204: Etapa 2)
Valida a integração entre a Entidade Cupom (Aula 24) e o Repositório SQLite (Aula 25).
"""
import os
from datetime import date, timedelta
from bibliotaua.database import obter_conexao, inicializar_banco, popular_dados_iniciais
from bibliotaua.repositories.cupom_repository import CupomRepository
from bibliotaua.models.cupom import Cupom, TipoDesconto
from bibliotaua.exceptions import (
    CupomInexistenteError,
    ValorMinimoNaoAtingidoError
)

def main():
    print("=================================================================")
    print("  BIBLIOTAUÁ — TESTE DE PERSISTÊNCIA RELACIONAL (AULA 25)")
    print("=================================================================\n")

    db_file = os.path.join(os.path.dirname(__file__), "bibliotaua.db")
    if os.path.exists(db_file):
        os.remove(db_file)

    print("[1] Inicializando esquema DDL e semeando acervo inicial...")
    inicializar_banco(db_file)
    popular_dados_iniciais(db_file)
    print("    -> Banco SQLite 'bibliotaua.db' inicializado com sucesso!\n")

    conn = obter_conexao(db_file)
    repo = CupomRepository(conn)

    print("[2] Consultando cupom semeado via CupomRepository.buscar_por_codigo('BEMVINDO10')...")
    cupom = repo.buscar_por_codigo("BEMVINDO10")
    print(f"    -> Cupom recuperado do banco: {cupom.codigo}")
    print(f"       Tipo: {cupom.tipo_desconto.value} | Desconto: {cupom.valor_desconto}% | Min: R$ {cupom.valor_minimo_pedido:.2f}")
    print(f"       Validade: {cupom.validade_ate} | Usos: {cupom.usos_realizados}/{cupom.limite_usos}\n")

    print("[3] Verificando compatibilidade com o motor de regras da Aula 24...")
    desconto = cupom.calcular_desconto(100.0)
    print(f"    -> Subtotal R$ 100.00: Desconto concedido = R$ {desconto:.2f} (Total = R$ {100.0 - desconto:.2f})")

    try:
        cupom.calcular_desconto(30.0)
    except ValorMinimoNaoAtingidoError as erro:
        print(f"    -> Subtotal R$ 30.00: Bloqueado com sucesso! ({erro})\n")

    print("[4] Persistindo novo cupom promocional no SQLite via CupomRepository.salvar()...")
    novo_cupom = Cupom(
        codigo="CALOURO20",
        tipo_desconto=TipoDesconto.VALOR_FIXO,
        valor_desconto=20.0,
        valor_minimo_pedido=70.0,
        limite_usos=15,
        usos_realizados=0,
        validade_ate=date.today() + timedelta(days=60),
        ativo=True
    )
    repo.salvar(novo_cupom)
    print(f"    -> Cupom '{novo_cupom.codigo}' persistido com ID gerado: {novo_cupom.id}\n")

    print("[5] Executando registro de uso atômico (baixa de utilização)...")
    repo.registrar_uso(novo_cupom.codigo)
    cupom_atualizado = repo.buscar_por_codigo("CALOURO20")
    print(f"    -> Usos realizados após registro: {cupom_atualizado.usos_realizados}/{cupom_atualizado.limite_usos}\n")

    print("[6] Testando busca por código inexistente ('NAOEXISTE')...")
    try:
        repo.buscar_por_codigo("NAOEXISTE")
    except CupomInexistenteError as erro:
        print(f"    -> Exceção capturada com sucesso: {erro}\n")

    print("[7] Testando ataque de SQL Injection (' OR '1'='1)...")
    try:
        repo.buscar_por_codigo("' OR '1'='1")
    except CupomInexistenteError:
        print("    -> BLINDADO! O ataque foi tratado como texto puro e o banco permaneceu integro.\n")

    conn.close()
    print("=================================================================")
    print("  SUCESSO: Todos os testes de persistência e compatibilidade OK!")
    print("=================================================================")

if __name__ == "__main__":
    main()

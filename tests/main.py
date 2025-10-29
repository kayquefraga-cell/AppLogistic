import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from confirmaPedidos import lambda_handler as confirma_pedidos
from calculaGeoLocalização import lambda_handler as calcula_geo
from processaPedidos import lambda_handler as processa_pedido


def main():
    print("\n=== SIMULAÇÃO DO FLUXO DE PEDIDOS ===\n")

    # 1️⃣ Criação e confirmação do pedido
    evento_pedido = {
        "cliente": "Kayque Fraga",
        "endereco": "Rua das Flores, 123 - São Paulo",
        "itens": ["Notebook", "Mouse Gamer"]
    }

    resposta_pedido = confirma_pedidos(evento_pedido)
    pedido_criado = json.loads(resposta_pedido["body"])
    pedido_id = pedido_criado["id"]

    print(f"[1] Pedido criado e confirmado: {pedido_id}\n")

    # 2️⃣ Calcula o galpão mais próximo (coordenadas simuladas de São Paulo)
    evento_geo = {
        "pedido_id": pedido_id,
        "localizacao": (-23.55052, -46.633308)  # São Paulo
    }

    resposta_geo = calcula_geo(evento_geo)
    pedido_atualizado = json.loads(resposta_geo["body"])

    print(f"[2] Galpão vinculado: {pedido_atualizado['galpao']['nome']}\n")

    # 3️⃣ Processa o pedido
    evento_proc = {"pedido_id": pedido_id}
    resposta_proc = processa_pedido(evento_proc)
    pedido_final = json.loads(resposta_proc["body"])

    print(f"[3] Pedido processado com sucesso!\n")
    print(json.dumps(pedido_final, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
from queue.filapedidos import filaPedidos
import json
import uuid
from datetime import datetime

def lambda_handler(event, context=None):
    with open("baseDadosPedidos.json", "r") as f:
        pedidos = json.load(f)

    novo_pedido = {
        "id": str(uuid.uuid4()),
        "cliente": event.get("cliente"),
        "endereco": event.get("endereco"),
        "itens": event.get("itens"),
        "status": "Confirmado",
        "data_pedido": datetime.now().isoformat()
    }

    pedidos.append(novo_pedido)

    with open("baseDadosPedidos.json", "w") as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)

    print(f"Pedido confirmado: {novo_pedido['id']}")
    return {"statusCode": 200, "body": json.dumps(novo_pedido)}
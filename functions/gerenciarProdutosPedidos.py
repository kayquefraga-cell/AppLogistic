import json
def lambda_handler(event, context=None):
    with open("baseDadosPedidos.json", "r") as f:
        pedidos = json.load(f)

    pedido = next((p for p in pedidos if p["id"] == event.get("pedido_id")), None)
    if not pedido:
        return {"statusCode": 404, "body": "Pedido não encontrado"}

    produtos_atualizados = event.get("produtos", [])
    pedido["itens"] = produtos_atualizados

    with open("baseDadosPedidos.json", "w") as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)

    print(f"Produtos do pedido {pedido['id']} atualizados com sucesso.")
    return {"statusCode": 200, "body": json.dumps(pedido)}
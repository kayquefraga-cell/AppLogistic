import json
import math

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def lambda_handler(event, context=None):
    with open("baseDadosPedidos.json", "r") as f:
        pedidos = json.load(f)

    with open("baseDadosGalpões.json", "r") as f:
        galpoes = json.load(f)

    pedido = next((p for p in pedidos if p["id"] == event.get("pedido_id")), None)
    if not pedido:
        return {"statusCode": 404, "body": "Pedido não encontrado"}

    lat_cliente, lon_cliente = event["localizacao"]

    galpao_mais_proximo = min(
        galpoes,
        key=lambda g: calcular_distancia(lat_cliente, lon_cliente, g["latitude"], g["longitude"])
    )

    pedido["galpao"] = galpao_mais_proximo
    pedido["status"] = "Aguardando processamento"

    with open("baseDadosPedidos.json", "w") as f:
        json.dump(pedidos, f, indent=4, ensure_ascii=False)

    print(f"Pedido {pedido['id']} vinculado ao galpão {galpao_mais_proximo['nome']}")
    return {"statusCode": 200, "body": json.dumps(pedido)}

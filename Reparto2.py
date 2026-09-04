import simpy
import random

# Parámetros
NUM_REPARTIDORES = 1
TIEMPO_SIMULACION = 120.0           # 120 min = 2 horas

# Tiempos
TIEMPO_COCINA = (18.0, 22.0)        # ~20 min
LLEGADA_LOCAL = (3.0, 5.0)          # <= 5 min
TRASLADO_CLIENTE = (8.0, 12.0)      # ~10 min
INTERVALO_PEDIDOS = (20.0, 25.0)    # tiempo entre pedidos


def pedido_process(env, id_pedido, repartidores, retraso_app, metricas):
    hora_solicitud = env.now
    print(f"[{env.now:6.2f}] E1 Orden #{id_pedido} generada")

    # Preparación en cocina
    comida_lista = env.timeout(random.uniform(*TIEMPO_COCINA))

    # Asignación del pedido y traslado del repartidor
    with repartidores.request() as req:
        yield req

        # Experimento: notificación retrasada de la App
        if retraso_app > 0:
            yield env.timeout(retraso_app)

        print(f"[{env.now:6.2f}] E2 Repartidor va al restaurante (Pedido #{id_pedido})")

        # Traslado al restaurante
        yield env.timeout(random.uniform(*LLEGADA_LOCAL))
        print(f"[{env.now:6.2f}] E2 Repartidor llega al local (Pedido #{id_pedido})")

        # Fila de espera en el local (si la comida aún no está lista)
        hora_arribo = env.now
        if not comida_lista.processed:
            print(f"[{env.now:6.2f}] E3 Repartidor en fila de espera (Pedido #{id_pedido})")
            yield comida_lista
        tiempo_espera_local = env.now - hora_arribo

        print(f"[{env.now:6.2f}] E4 Repartidor recibe el pedido #{id_pedido}")

        # Traslado final hacia el cliente
        yield env.timeout(random.uniform(*TRASLADO_CLIENTE))

        # Guardar métricas
        metricas['espera_wq'].append(tiempo_espera_local)
        metricas['total_w'].append(env.now - hora_solicitud)

        print(f"[{env.now:6.2f}] E5 Pedido #{id_pedido} entregado. Repartidor queda Libre "
              f"(ciclo: {env.now - hora_solicitud:.2f} min)")


def generador_pedidos(env, repartidores, retraso_app, metricas):
    id_pedido = 1
    while True:
        env.process(pedido_process(env, id_pedido, repartidores, retraso_app, metricas))
        yield env.timeout(random.uniform(*INTERVALO_PEDIDOS))
        id_pedido += 1


def simular(retraso_app=0.0):
    random.seed(42)
    env = simpy.Environment()
    repartidores = simpy.Resource(env, capacity=NUM_REPARTIDORES)
    metricas = {'espera_wq': [], 'total_w': []}

    modo = "Escenario Base" if retraso_app == 0 else f"Experimento (Retraso {retraso_app} min)"
    print(f"\n=== {modo} ===")

    env.process(generador_pedidos(env, repartidores, retraso_app, metricas))
    env.run(until=TIEMPO_SIMULACION)

    completados = len(metricas['total_w'])
    wq_prom = sum(metricas['espera_wq']) / completados if completados else 0
    w_prom = sum(metricas['total_w']) / completados if completados else 0

    print(f"\n--- Resultados: {modo} ---")
    print(f"• Pedidos entregados: {completados}")
    print(f"• Tiempo muerto promedio en restaurante (Wq): {wq_prom:.2f} min")
    print(f"• Tiempo total de servicio promedio (W):     {w_prom:.2f} min\n")


if __name__ == "__main__":
    simular(retraso_app=0.0)   # Asignación inmediata de la App
    simular(retraso_app=11.0)  # Asignación diferida 11 minutos

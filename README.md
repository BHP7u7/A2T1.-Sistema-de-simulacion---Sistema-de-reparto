# A2T1.-Sistema-de-simulacion  / Sistema-de-reparto
Simulación de un sistema de reparto de comida con repartidores, tiempos de cocina, traslados y retrasos. 

Alumnos:

-Dzib Pool Jose Francisco

-Hoil Puc Brian

Este programa simula un sistema de reparto de comida a domicilio utilizando SimPy. El modelo muetra el flujo completo de un pedido, desde que es generado por un cliente hasta que es entregado por un repartidor, considerando:

- Tiempo de preparación en cocina.
- Asignación y traslado de repartidores.
- Tiempos de espera en el restaurante.
- Métricas como tiempo en cola (Wq) y tiempo total de servicio (W).

  (Extra)
- Notificaciones de la aplicación (con posibilidad de retraso).
  


Lógica del modelo
1. Generación de pedidos: Cada cierto intervalo (entre 20 y 25 minutos), se genera un nuevo pedido
2. Preparación en cocina: Toma ~20 (entre 18 y 22 minutos)
3. Asignación de repartidor: El repartidor es asignado cuando está disponible
4. Traslado al restaurante: Tarda entre 3 y 5 minutos
5. Espera en el local: Si la comida no está lista, el repartidor espera
6. Entrega al cliente: El viaje final toma ~10 (entre 8 y 12 minutos)



Que se muestra:
- Escenario base: Asignación inmediata del repartidor al pedido.
- Experimento: La app notifica al repartidor con 11 minutos de retraso.



Al final se calcula:
- Wq: Tiempo promedio que el repartidor espera en el restaurante.
- W: Tiempo promedio total desde que se genera el pedido hasta que se entrega.

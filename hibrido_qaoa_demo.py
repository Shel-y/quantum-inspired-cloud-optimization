import boto3

from braket.circuits import Circuit, FreeParameter

from braket.devices import LocalSimulator


# 1. Preparamos todo para llamar a CloudWatch

# Asegúrate de que la región sea la misma donde estás trabajando (ej. us-east-1)

cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')


def enviar_metrica(nombre, valor):

    try:

        cloudwatch.put_metric_data(
            # Aqui puedes cambiar el nombre
            Namespace='QuantumDemo/Optimizacion',

            MetricData=[

                {

                    'MetricName': nombre,

                    'Value': float(valor),
                    #puedes cambiarlo a las unidades que necesites (ej.milliseconds)
                    'Unit': 'None'

                },

            ]

        )

        print(f"[CloudWatch] Métrica '{nombre}' enviada exitosamente con valor: {valor}")

    except Exception as e:

        print(f" Error de permisos en CloudWatch: {e}")


def optimizacion_hibrida_demo():

    print(" INICIANDO OPTIMIZACIÓN HÍBRIDA (EC2 + QUANTUM)")

    print("-" * 50)

    

    theta = FreeParameter("theta")

    circuito = Circuit().rx(0, theta).rx(1, theta).cz(0, 1)

    device = LocalSimulator()

    

    angulos_a_probar = [0.0, 0.5, 1.0, 1.5, 3.14] 

    mejor_angulo = 0.0

    mejor_puntaje = 0

    

    print(" La EC2 clásica comienza a ajustar las configuraciones...\n")

    

    for angulo in angulos_a_probar:

        print(f" EC2 prueba en: {angulo}")

        tarea = device.run(circuito, shots=100, inputs={"theta": angulo})

        resultado = tarea.result().measurement_counts

        print(f"Braket evalúa y responde: {resultado}")

        

        puntaje_actual = resultado.get('11', 0)

        

        if puntaje_actual > mejor_puntaje:

            mejor_puntaje = puntaje_actual

            mejor_angulo = angulo


    print("\n" + "="*50)

    print(" ¡OPTIMIZACIÓN COMPLETADA CON ÉXITO!")

    print("="*50)

    print(f"Configuración perfecta: {mejor_angulo}")

    print(f"Validación cuántica: {mejor_puntaje} / 100")

    

    # 2. Enviamos los resultados a CloudWatch

    print("\n Enviando resultados al panel de telemetría de AWS...")

    enviar_metrica('MejorAngulo_Theta', mejor_angulo)

    enviar_metrica('PuntajeDeValidacion', mejor_puntaje)


# Ejecutar el demo

optimizacion_hibrida_demo()

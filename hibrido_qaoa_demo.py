import boto3
import csv
import os
from braket.circuits import Circuit, FreeParameter
from braket.devices import LocalSimulator

# ==========================================
# 1. CONFIGURACIÓN DE AWS
# ==========================================
# Cambia esto por el nombre real de tu bucket en tu cuenta
BUCKET_NAME = 'shel-quantum-demo-data-2026' 
REGION = 'us-east-1'

s3 = boto3.client('s3', region_name=REGION)
cloudwatch = boto3.client('cloudwatch', region_name=REGION)

def enviar_metrica(nombre, valor, dimensiones=None):
    """Envía métricas a CloudWatch, opcionalmente con etiquetas (dimensiones)."""
    metric_data = {
        'MetricName': nombre, 
        'Value': float(valor), 
        'Unit': 'None'
    }
    
    if dimensiones:
        metric_data['Dimensions'] = dimensiones

    try:
        cloudwatch.put_metric_data(
            Namespace='QuantumDemo/Optimizacion',
            MetricData=[metric_data]
        )
    except Exception as e:
        print(f" Error al enviar a CloudWatch: {e}")

# ==========================================
# 2. PIPELINE HÍBRIDO PRINCIPAL
# ==========================================
def optimizacion_hibrida_demo():
    print("INICIANDO PIPELINE: S3 -> EC2 -> QUANTUM -> CLOUDWATCH")
    print("-" * 60)

    # --- Descarga de Datos  ---
    print(f" Descargando inventario desde S3: s3://{BUCKET_NAME}/configs.csv...")
    if not os.path.exists('configs.csv'):
        try:
            s3.download_file(BUCKET_NAME, 'configs.csv', 'configs.csv')
            print(" Archivo descargado exitosamente.")
        except Exception as e:
            print(f" No se pudo bajar de S3 (usando archivo local si existe): {e}")
    else:
        print(" Usando archivo configs.csv local existente.")

    # --- Filtrado de Cuellos de Botella ---
    print("\n Analizando métricas clásicas para identificar nodos críticos...")
    
    with open('configs.csv', mode='r') as file:
        reader = csv.DictReader(file)
        # Ordenamos por consumo de CPU de mayor a menor y tomamos los top 2
        datos = sorted(reader, key=lambda x: float(x['cpu']), reverse=True)
        tops = datos[:2]
        ids_criticos = [row['instance_id'] for row in tops]
    
    objetivo = '11' # El estado '11' representa ambos nodos entrelazados/activos
    print(f"Nodos con mayor carga de CPU detectados: {ids_criticos}")
    print(f"Objetivo Cuántico: Evaluar estabilidad de la topología '{objetivo}'\n")

    # --- Algoritmo Variacional  ---
    theta = FreeParameter("theta")
    circuito = Circuit().rx(0, theta).rx(1, theta).cz(0, 1)
    device = LocalSimulator()
    
    mejores = {'angulo': 0.0, 'puntaje': 0}
    angulos_a_probar = [0.0, 0.5, 1.0, 1.5, 3.14]
    
    print(" EC2 iterando hiperparámetros y Braket evaluando probabilidades...")
    for angulo in angulos_a_probar:
        tarea = device.run(circuito, shots=100, inputs={"theta": angulo})
        resultado = tarea.result().measurement_counts
        
        # Buscamos cuántas veces salió nuestro estado objetivo ('11')
        puntaje = resultado.get(objetivo, 0)
        print(f"  Theta en {angulo:.2f} | Confianza de la topología: {puntaje}%")
        
        if puntaje > mejores['puntaje']:
            mejores['puntaje'] = puntaje
            mejores['angulo'] = angulo

    print("\n" + "="*50)
    print(" RESULTADO DE LA OPTIMIZACIÓN Y DECISIÓN")
    print("="*50)
    
    # 1 (Acción requerida: Aislar) o 0 (No aislar)
    decision = 1 if mejores['puntaje'] > 80 else 0
    
    # Creamos las dimensiones con los IDs reales extraídos del CSV
    etiquetas_nodos = [
        {'Name': 'NodoCritico_A', 'Value': str(ids_criticos[0])},
        {'Name': 'NodoCritico_B', 'Value': str(ids_criticos[1])}
    ]

    if decision == 1:
        print(f" ACCIÓN RECOMENDADA: Aislar en clúster dedicado los nodos {ids_criticos}")
        print(f"   Motivo: Alta confianza cuántica ({mejores['puntaje']}%) en el estado entrelazado.")
    else:
        print(f" ACCIÓN RECOMENDADA: No aislar. Apagar/Redimensionar nodos {ids_criticos}")
        print(f"   Motivo: Confianza cuántica insuficiente ({mejores['puntaje']}%). Riesgo de latencia.")

    print("\nEnviando telemetría etiquetada al Dashboard de CloudWatch...")
    enviar_metrica('Confianza_Topologia', mejores['puntaje'], etiquetas_nodos)
    enviar_metrica('Decision_Aislar_Nodos', decision, etiquetas_nodos)
    print(" Demo finalizada con éxito.")

if __name__ == "__main__":
    optimizacion_hibrida_demo()

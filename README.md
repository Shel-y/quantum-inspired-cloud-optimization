# ⚛️ Optimización de Nube Híbrida (Clásico-Cuántico) con AWS

Este repositorio contiene el código fuente de la demostración presentada en la charla **"De lo Clásico a lo Cuántico con AWS"** durante el **AWSome Women Summit LATAM 2026**.

## 🎯 El Problema
A medida que las arquitecturas de microservicios escalan, encontrar la topología de red óptima para aislar nodos críticos se vuelve un problema matemático complejo. Las reglas de auto-escalado tradicionales a menudo reaccionan tarde o dejan infraestructura ociosa.

## 💡 La Solución Híbrida
Este proyecto demuestra cómo utilizar un **Algoritmo Cuántico Variacional (inspirado en QAOA)** para tomar decisiones arquitectónicas proactivas. Unimos el poder de orquestación de la nube clásica con la exploración estocástica del cómputo cuántico.

### Flujo de la Arquitectura (Pipeline)
1. **Ingesta (Amazon S3):** Descarga de un inventario simulado (`configs.csv`) con métricas operativas de infraestructura.
2. **Orquestador Clásico (Amazon EC2):** Filtra los nodos con mayor estrés de CPU y ajusta los hiperparámetros (ángulo $\theta$) del circuito cuántico.
3. **Coprocesador Cuántico (AWS Braket - LocalSimulator):** Ejecuta el circuito parametrizado para evaluar matemáticamente la estabilidad de entrelazar los nodos críticos (estado `11`).
4. **Observabilidad (Amazon CloudWatch):** Traduce el resultado cuántico en una decisión binaria (Aislar / No Aislar) y envía la telemetría para alertado en tiempo real.

## 🗺️ Arquitectura
<p align="center">
  <img src="./assets/S3.png" alt="Diagrama de Arquitectura de Nube Híbrida" width="600"/>
</p>

## ⚙️ Requisitos Previos
* Cuenta de AWS activa.
* Rol de IAM con permisos para `s3:GetObject` y `cloudwatch:PutMetricData`.
* Python 3.8+
* Librerías: `boto3`, `amazon-braket-sdk`

## 🚀 Ejecución

1. Clona este repositorio y configura tus credenciales de AWS CLI.
2. Asegúrate de tener un bucket de S3 con el archivo `configs.csv` (o deja que el script lea la versión local incluida).
3. Ejecuta el pipeline:
   ```bash
   python hibrido_qaoa_demo.py
   ```

import time
import matplotlib.pyplot as plt

def leer_secuencia_desde_archivo(nombre_archivo):
    """
    Lee una secuencia de ADN desde un archivo de texto y valida los caracteres.
    Args:
        nombre_archivo (str): Ruta del archivo .txt.
    Returns:
        str: Secuencia de ADN válida.
    Raises:
        ValueError: Si la secuencia contiene caracteres no válidos.
    """
    with open(nombre_archivo, 'r') as archivo:
        secuencia = archivo.read().strip().upper()
    
    # Validación de nucleótidos
    nucleotidos_validos = {'A', 'T', 'C', 'G'}
    for i, nucleotido in enumerate(secuencia):
        if nucleotido not in nucleotidos_validos:
            raise ValueError(f"Carácter no válido '{nucleotido}' en posición {i}. Solo se permiten A, T, C, G.")
    
    return secuencia

def detectar_mutaciones(secuencia_referencia, secuencia_muestra):
    """
    Detecta mutaciones y diferencias de longitud.
    Args:
        secuencia_referencia (str): Secuencia de referencia.
        secuencia_muestra (str): Secuencia del sensor.
    Returns:
        tuple: (mutaciones, mensaje_advertencia)
    """
    mutaciones = []
    min_longitud = min(len(secuencia_referencia), len(secuencia_muestra))
    
    for i in range(min_longitud):
        if secuencia_referencia[i] != secuencia_muestra[i]:
            mutaciones.append(i)
    
    mensaje_advertencia = None
    if len(secuencia_referencia) != len(secuencia_muestra):
        mensaje_advertencia = f"¡Advertencia! Longitudes distintas. Referencia: {len(secuencia_referencia)}, Muestra: {len(secuencia_muestra)}"
    
    return mutaciones, mensaje_advertencia

def visualizar_mutaciones(secuencia_referencia, secuencia_muestra, mutaciones):
    """
    Genera un gráfico que muestra las mutaciones.
    Args:
        secuencia_referencia (str): Secuencia de referencia.
        secuencia_muestra (str): Secuencia del sensor.
        mutaciones (list): Posiciones de mutaciones.
    """
    plt.figure(figsize=(10, 4))
    plt.title("Monitorización de Mutaciones en Tiempo Real")
    
    # Crear listas para los puntos de referencia y muestra
    x_ref = range(len(secuencia_referencia))
    x_muestra = range(len(secuencia_muestra))
    
    # Graficar secuencias
    plt.plot(x_ref, [1] * len(x_ref), 'o', color='blue', label='Referencia')
    plt.plot(x_muestra, [0.5] * len(x_muestra), 'o', color='green', label='Muestra')
    
    # Marcar mutaciones
    for pos in mutaciones:
        if pos < len(secuencia_muestra) and pos < len(secuencia_referencia):
            plt.plot([pos, pos], [1, 0.5], 'r--', linewidth=0.5)
            plt.text(pos, 0.75, f"{secuencia_referencia[pos]}→{secuencia_muestra[pos]}", 
                     ha='center', color='red', fontsize=8)
    
    plt.yticks([1, 0.5], ["Referencia", "Muestra"])
    plt.xlabel("Posición en la secuencia")
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig("mutaciones.png")  # Guardar imagen
    plt.show()

def monitorizar_continuamente(archivo_sensor, intervalo=5):
    """
    Monitoriza el archivo del sensor en intervalos regulares.
    Args:
        archivo_sensor (str): Ruta del archivo.
        intervalo (int): Segundos entre lecturas.
    """
    referencia = "ATGCTAGCTAAT"
    print(f"\nIniciando monitorización cada {intervalo} segundos. Presiona Ctrl+C para detener.\n")
    
    try:
        while True:
            try:
                secuencia = leer_secuencia_desde_archivo(archivo_sensor)
                mutaciones, advertencia = detectar_mutaciones(referencia, secuencia)
                
                print(f"\n--- Análisis: {time.ctime()} ---")
                if mutaciones:
                    print("Mutaciones detectadas:")
                    for pos in mutaciones:
                        print(f"  Posición {pos}: {referencia[pos]} → {secuencia[pos]}")
                else:
                    print("No hay mutaciones detectadas.")
                
                if advertencia:
                    print(advertencia)
                
                visualizar_mutaciones(referencia, secuencia, mutaciones)
                time.sleep(intervalo)
            
            except ValueError as e:
                print(f"Error: {e}")
                time.sleep(intervalo)
    
    except KeyboardInterrupt:
        print("\nMonitorización detenida.")

# --- Ejecución principal ---
if __name__ == "__main__":
    ARCHIVO_SENSOR = "sensor_data.txt"
    
    # Ejemplo de uso con las 3 mejoras:
    monitorizar_continuamente(ARCHIVO_SENSOR, intervalo=5)
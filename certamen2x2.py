import requests

def obtener_coordenadas(ciudad):
    # Diccionario con las coordenadas de Santiago y La Serena
    ciudades = {
        'santiago': {'lat': -33.4489, 'lng': -70.6693},
        'la serena': {'lat': -29.9027, 'lng': -71.2519},
    }
    return ciudades.get(ciudad.lower(), None)  # Convertimos la ciudad a minúsculas para evitar errores


def calcular_combustible(distancia_km, consumo_por_km=0.12):
    # Estimación del consumo de combustible (0.12 litros/km por defecto)
    return distancia_km * consumo_por_km


def obtener_distancia_y_duracion(origen, destino, api_key):
    coordenadas_origen = obtener_coordenadas(origen)
    coordenadas_destino = obtener_coordenadas(destino)

    if not coordenadas_origen or not coordenadas_destino:
        print("Error: Una de las ciudades no tiene coordenadas disponibles.")
        return None

    url = f"https://graphhopper.com/api/1/route?point={coordenadas_origen['lat']},{coordenadas_origen['lng']}&point={coordenadas_destino['lat']},{coordenadas_destino['lng']}&vehicle=car&locale=es&key={api_key}&type=json"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        distancia_km = data['paths'][0]['distance'] / 1000  # Convertir de metros a kilómetros
        duracion_segundos = data['paths'][0]['time'] / 1000  # Convertir de milisegundos a segundos
        return distancia_km, duracion_segundos
    else:
        print(f"Error al obtener los datos de la API: {response.status_code}")
        return None


def convertir_duracion(duracion_segundos):
    horas = int(duracion_segundos // 3600)
    minutos = int((duracion_segundos % 3600) // 60)
    segundos = int(duracion_segundos % 60)
    return horas, minutos, segundos


def imprimir_narrativa(origen, destino, distancia_km, horas, minutos, segundos, combustible_litros):
    print("\n--- Detalles del Viaje ---")
    print(f"Ciudad de origen: {origen}")
    print(f"Ciudad de destino: {destino}")
    print(f"Distancia: {distancia_km:.2f} km")
    print(f"Duración del viaje: {horas} horas, {minutos} minutos y {segundos} segundos")
    print(f"Combustible estimado requerido: {combustible_litros:.2f} litros")
    print(f"\nNarrativa: El viaje desde {origen} hasta {destino} cubre una distancia de aproximadamente {distancia_km:.2f} kilómetros. "
          f"Se espera que dure alrededor de {horas} horas, {minutos} minutos y {segundos} segundos. Para completar el viaje, "
          f"se requerirán aproximadamente {combustible_litros:.2f} litros de combustible.")


def main():
    while True:
        # Solicitar la ciudad de origen y destino
        origen = input("Ingrese la ciudad de origen (Santiago/La Serena o 'q'/'Quit' para salir): ").strip()
        if origen.lower() in ['q', 'quit']:
            print("Saliendo del programa...")
            break

        destino = input("Ingrese la ciudad de destino (Santiago/La Serena o 'q'/'Quit' para salir): ").strip()
        if destino.lower() in ['q', 'quit']:
            print("Saliendo del programa...")
            break

        # Verificar que las ciudades ingresadas estén disponibles
        if origen.lower() == destino.lower():
            print("La ciudad de origen y destino no pueden ser iguales.")
            continue

        # Inserta tu API key de GraphHopper aquí
        api_key = '5da09757-2f24-41e5-bdff-6ac196678aad'

        # Obtener la distancia y duración del viaje
        resultado = obtener_distancia_y_duracion(origen, destino, api_key)
        if resultado:
            distancia_km, duracion_segundos = resultado

            # Convertir la duración de segundos a horas, minutos y segundos
            horas, minutos, segundos = convertir_duracion(duracion_segundos)

            # Calcular el combustible requerido
            combustible_litros = calcular_combustible(distancia_km)

            # Imprimir la narrativa del viaje
            imprimir_narrativa(origen, destino, distancia_km, horas, minutos, segundos, combustible_litros)


if __name__ == "__main__":
    main()

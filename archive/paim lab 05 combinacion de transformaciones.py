import streamlit as st
import cv2
import numpy as np
import imageio

# Función para leer y convertir una imagen a escala de grises
def leer_imagen(archivo_imagen):
    imagen_bytes = archivo_imagen.read()
    imagen = imageio.imread(imagen_bytes, pilmode="L")
    return imagen

# # Función para leer y convertir una imagen a escala de grises
# def leer_imagen(archivo_imagen):
#     imagen_bytes = archivo_imagen.read()
#     imagen_array = np.frombuffer(imagen_bytes, np.uint8)
#     imagen = cv2.imdecode(imagen_array, cv2.IMREAD_UNCHANGED)
#     if len(imagen.shape) == 3:
#         imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
#     else:
#         imagen_gris = imagen
#     return imagen_gris


# Función para aplicar un umbral variable a la imagen en escala de grises
def aplicar_umbral(imagen_gris, umbral):
    _, imagen_umbralizada = cv2.threshold(imagen_gris, umbral, 255, cv2.THRESH_BINARY)
    return imagen_umbralizada

# Función para aplicar una transformación morfológica a la imagen umbralizada
def aplicar_transformacion_morfologica(imagen_umbralizada, tipo_transformacion, tamano_kernel, num_iteraciones):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (tamano_kernel, tamano_kernel))
    if tipo_transformacion == "dilatacion":
        imagen_resultado = cv2.dilate(imagen_umbralizada, kernel, iterations=num_iteraciones)
    elif tipo_transformacion == "erosion":
        imagen_resultado = cv2.erode(imagen_umbralizada, kernel, iterations=num_iteraciones)
    elif tipo_transformacion == "apertura":
        imagen_resultado = cv2.morphologyEx(imagen_umbralizada, cv2.MORPH_OPEN, kernel, iterations=num_iteraciones)
    elif tipo_transformacion == "cierre":
        imagen_resultado = cv2.morphologyEx(imagen_umbralizada, cv2.MORPH_CLOSE, kernel, iterations=num_iteraciones)
    elif tipo_transformacion == "gradiente":
        imagen_resultado = cv2.morphologyEx(imagen_umbralizada, cv2.MORPH_GRADIENT, kernel, iterations=num_iteraciones)
    else:
        imagen_resultado = imagen_umbralizada
    return imagen_resultado

def main():
    st.title("Aplicación de transformaciones morfológicas")
    archivo_imagen = st.file_uploader("Seleccione una imagen", type=["jpg", "jpeg", "png", "gif", "webp"])

    if archivo_imagen is not None:
        # Leer la imagen y convertirla a escala de grises
        imagen_gris = leer_imagen(archivo_imagen)
        st.image(imagen_gris, caption="Imagen original en escala de grises")

        # Aplicar umbral variable a la imagen en escala de grises
        umbral = st.slider("Umbral", 0, 255, 127)
        imagen_umbralizada = aplicar_umbral(imagen_gris, umbral)
        st.image(imagen_umbralizada, caption="Imagen umbralizada")

        # Aplicar transformación morfológica a la imagen umbralizada
        tipo_transformacion = st.selectbox("Tipo de transformación morfológica", ["ninguna", "dilatacion", "erosion", "apertura", "cierre", "gradiente"])
        if tipo_transformacion != "ninguna":
            tamano_kernel = st.slider("Tamaño del kernel", 1, 21, 3, step=2)
            num_iteraciones = st.slider("Número de iteraciones", 1, 10, 1)
            imagen_resultado = aplicar_transformacion_morfologica(imagen_umbralizada, tipo_transformacion, tamano_kernel, num_iteraciones)
            st.image(imagen_resultado, caption="Imagen resultante")
        else:
            imagen_resultado = imagen_umbralizada

        # Mostrar una comparación entre la imagen original y la imagen resultante
        imagenes_comparacion = np.concatenate((imagen_gris, imagen_resultado), axis=1)
        st.image(imagenes_comparacion, caption="Comparación entre la imagen original y la imagen resultante")


main()
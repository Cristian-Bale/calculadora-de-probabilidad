import streamlit as st
import random

import copy
import random

class Hat:
    
    def __init__(self, **kwargs):
        self.contents = []

        for color, count in kwargs.items():
            self.contents.extend([color] * count)

    def draw(self, num_balls_drawn):
        
        if num_balls_drawn >= len(self.contents):
            drawn_balls = self.contents
            self.contents = []
            return drawn_balls
        
        drawn_balls = []
        for _ in range(num_balls_drawn):
            chosen_ball = random.choice(self.contents)
            drawn_balls.append(chosen_ball)

            self.contents.remove(chosen_ball)

        return drawn_balls


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    
    M = 0

    for _ in range(num_experiments):
        temp_hat = copy.deepcopy(hat)

        drawn_balls = temp_hat.draw(num_balls_drawn)

        drawn_counts = {}

        for ball in drawn_balls:
            drawn_counts[ball] = drawn_counts.get(ball, 0) + 1 

        success = True

        for color, count in expected_balls.items():
            if drawn_counts.get(color, 0) < count:
                success = False
                break

        if success:

            M += 1 

    return M / num_experiments



st.set_page_config(page_title="Calculadora de Probabilidad Monte Carlo", layout="wide")
st.title("🎩 Calculadora de Probabilidad por Simulación")
st.markdown("Estima la probabilidad de obtener un conjunto específico de bolas de un sombrero.")

# --- 1. Definir el Sombrero (Sidebar) ---
st.sidebar.header("1. Definir el Sombrero")
st.sidebar.markdown("Introduce la cantidad de cada color que hay en el sombrero.")
colores = ['Rojo', 'Azul', 'Verde', 'Amarillo', 'Negro']
hat_definition = {}

for color in colores:
    count = st.sidebar.number_input(f"Bolas {color}:", min_value=0, value=0, key=f"hat_{color}")
    if count > 0:
        hat_definition[color.lower()] = count

if not hat_definition:
    st.warning("Define al menos una bola en el sombrero (usando la barra lateral).")
    st.stop()


# --- 2. Definir el Experimento (Main Panel) ---
st.header("2. Configuración del Experimento")
num_experiments = st.number_input("Número de Experimentos a Realizar:", min_value=100, value=5000)
num_balls_drawn = st.number_input("Número de Bolas a Extraer en cada Intento:", min_value=1, value=4)

if num_balls_drawn > sum(hat_definition.values()):
    st.warning("El número de bolas a extraer es mayor que el total de bolas en el sombrero.")


# --- 3. Definir las Bolas Esperadas ---
st.header("3. Bolas Esperadas para el Éxito")
st.markdown("Especifica el mínimo de cada color que debe obtenerse.")
expected_balls = {}

cols = st.columns(len(colores))
for i, color in enumerate(colores):
    with cols[i]:
        expected_count = st.number_input(f"{color} mín:", min_value=0, value=0, key=f"exp_{color}")
        if expected_count > 0:
            expected_balls[color.lower()] = expected_count

if not expected_balls:
    st.warning("Define al menos una condición de éxito (ej: 1 Roja).")
    st.stop()


# --- 4. Ejecutar y Mostrar Resultado ---

if st.button("Calcular Probabilidad"):
    
    # 1. Crear el objeto Hat a partir de la definición del usuario
    initial_hat = Hat(**hat_definition)
    
    with st.spinner('Realizando la simulación...'):
        # 2. Ejecutar la función experiment
        probability = experiment(
            hat=initial_hat,
            expected_balls=expected_balls,
            num_balls_drawn=num_balls_drawn,
            num_experiments=num_experiments
        )

    st.success("¡Cálculo Completo!")
    st.metric(label="Probabilidad Estimada (M/N)", value=f"{probability:.4f}", delta=f"Base en {num_experiments} experimentos")
    
    st.info(f"El sombrero inicial contenía: {initial_hat.contents}")
    st.info(f"Condición de éxito: {expected_balls} extraídas en {num_balls_drawn} intentos.")

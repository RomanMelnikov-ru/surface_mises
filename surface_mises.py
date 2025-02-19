import streamlit as st
import numpy as np
import plotly.graph_objs as go

# Функция для построения цилиндра Мизеса
def plot_mises_criterion(sigma_y, z_range):
    # Радиус цилиндра в девиаторной плоскости
    radius = np.sqrt(2 / 3) * sigma_y
    # Создание сетки для цилиндра
    theta = np.linspace(0, 2 * np.pi, 100)  # Угол для окружности
    z = np.linspace(0, z_range, 100)  # Ось цилиндра (гидростатическая ось, только положительная область)
    Theta, Z = np.meshgrid(theta, z)
    # Координаты цилиндра в девиаторной плоскости
    X = radius * np.cos(Theta)
    Y = radius * np.sin(Theta)
    # Преобразование в пространство главных напряжений
    # Гидростатическая ось: sigma1 = sigma2 = sigma3 = Z / sqrt(3)
    # Ось sigma1 — вертикальная
    sigma1 = X / np.sqrt(2) - Y / np.sqrt(6) + Z / np.sqrt(3)  # Вертикальная ось
    sigma2 = -X / np.sqrt(2) - Y / np.sqrt(6) + Z / np.sqrt(3)  # Горизонтальные оси
    sigma3 = 2 * Y / np.sqrt(6) + Z / np.sqrt(3)

    # Создание 3D-графика с помощью Plotly
    fig = go.Figure(data=[
        go.Surface(
            x=sigma1, y=sigma2, z=sigma3,
            colorscale="Blues",
            opacity=0.9,
            showscale=False,  # Убираем цветовую шкалу
            name="Поверхность Мизеса"
        )
    ])

    # Добавление гидростатической оси
    hydrostatic_line = np.linspace(0, z_range, 20)  # Только положительная область
    fig.add_trace(
        go.Scatter3d(
            x=hydrostatic_line,
            y=hydrostatic_line,
            z=hydrostatic_line,
            mode="lines",
            line=dict(color="gray", width=2, dash="dash"),
            name="Гидростатическая ось"
        )
    )

    # Добавление осей координат
    axis_range = np.linspace(0, z_range, 100)  # Только положительная область
    arrow_length = z_range * 0.1  # Длина стрелок
    arrow_head_size = z_range * 0.05  # Размер головки стрелки

    # Ось σ₂
    fig.add_trace(
        go.Scatter3d(
            x=[0, z_range, z_range + arrow_length],
            y=[0, 0, 0],
            z=[0, 0, 0],
            mode="lines",
            line=dict(color="blue", width=2),
            name="σ₂"
        )
    )
    # Стрелка для оси σ₂
    fig.add_trace(
        go.Cone(
            x=[z_range + arrow_length - arrow_head_size],
            y=[0],
            z=[0],
            u=[arrow_head_size],
            v=[0],
            w=[0],
            colorscale=[[0, "blue"], [1, "blue"]],
            showscale=False,
            sizemode="absolute",
            sizeref=arrow_head_size * 2
        )
    )

    # Ось σ₃
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[0, z_range, z_range + arrow_length],
            z=[0, 0, 0],
            mode="lines",
            line=dict(color="green", width=2),
            name="σ₃"
        )
    )
    # Стрелка для оси σ₃
    fig.add_trace(
        go.Cone(
            x=[0],
            y=[z_range + arrow_length - arrow_head_size],
            z=[0],
            u=[0],
            v=[arrow_head_size],
            w=[0],
            colorscale=[[0, "green"], [1, "green"]],
            showscale=False,
            sizemode="absolute",
            sizeref=arrow_head_size * 2
        )
    )

    # Ось σ₁
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[0, 0],
            z=[0, z_range, z_range + arrow_length],
            mode="lines",
            line=dict(color="red", width=2),
            name="σ₁"
        )
    )
    # Стрелка для оси σ₁
    fig.add_trace(
        go.Cone(
            x=[0],
            y=[0],
            z=[z_range + arrow_length - arrow_head_size],
            u=[0],
            v=[0],
            w=[arrow_head_size],
            colorscale=[[0, "red"], [1, "red"]],
            showscale=False,
            sizemode="absolute",
            sizeref=arrow_head_size * 2
        )
    )

    # Настройка макета графика
    fig.update_layout(
        title=f"Геометрическое представление критерия Мизеса (σᵧ = {sigma_y})",
        scene=dict(
            xaxis_title="σ₂",
            yaxis_title="σ₃",
            zaxis_title="σ₁",
            aspectmode="cube"
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        showlegend=True  # Показываем легенду только для общего графика
    )

    return fig

# Основной код Streamlit
st.title("Геометрическое представление критерия Мизеса")
# Слайдер для выбора предела текучести
sigma_y = st.slider(
    "Предел текучести (σᵧ):",
    min_value=5.0,
    max_value=50.0,
    value=20.0,
    step=5.0,
)
# Фиксированный диапазон для оси Z
z_range = 100.0
# Построение графика
fig = plot_mises_criterion(sigma_y, z_range)
st.plotly_chart(fig, use_container_width=True)

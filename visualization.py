# -*- coding: utf-8 -*-
"""
Módulo de visualizaciones para la aplicación Streamlit
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def plot_historical_population(df_stats):
    """Gráfico de población histórica"""
    fig = px.line(
        df_stats, 
        x='AÑO', 
        y='TOTAL',
        title='Evolución de la Población de Antioquia (1985-2025)',
        labels={'AÑO': 'Año', 'TOTAL': 'Población Total'},
        line_shape='linear'
    )
    
    fig.update_traces(
        mode='lines+markers',
        line=dict(width=3, color='#1f77b4'),
        marker=dict(size=6)
    )
    
    fig.update_layout(
        title_x=0.5,
        xaxis_title="Año",
        yaxis_title="Población Total",
        hovermode='x unified',
        template='plotly_white',
        height=500
    )
    
    return fig

def plot_real_vs_predicted(comparison):
    """Gráfico comparativo real vs predicción"""
    fig = go.Figure()
    
    # Valores reales
    fig.add_trace(go.Scatter(
        x=comparison['AÑO'],
        y=comparison['TOTAL'],
        mode='lines+markers',
        name='Población Real',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    # Predicciones
    fig.add_trace(go.Scatter(
        x=comparison['AÑO'],
        y=comparison['PREDICCION'],
        mode='lines+markers',
        name='Predicción del Modelo',
        line=dict(color='#ff7f0e', width=3, dash='dash'),
        marker=dict(size=8, symbol='x')
    ))
    
    fig.update_layout(
        title='Comparación: Población Real vs Predicción del Modelo (2016-2025)',
        title_x=0.5,
        xaxis_title="Año",
        yaxis_title="Población Total",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

def plot_future_predictions(df_model, future_predictions):
    """Gráfico con datos históricos y predicciones futuras"""
    fig = go.Figure()
    
    # Datos históricos
    fig.add_trace(go.Scatter(
        x=df_model['AÑO'],
        y=df_model['TOTAL'],
        mode='lines+markers',
        name='Datos Históricos',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))
    
    # Predicciones futuras
    fig.add_trace(go.Scatter(
        x=future_predictions['AÑO'],
        y=future_predictions['PREDICCION_TOTAL'],
        mode='lines+markers',
        name='Predicciones 2026-2050',
        line=dict(color='#d62728', width=3, dash='dot'),
        marker=dict(size=6, symbol='diamond')
    ))
    
    # Línea divisoria
    fig.add_vline(
        x=2025, 
        line_dash="dash", 
        line_color="gray",
        annotation_text="Inicio Predicciones"
    )
    
    fig.update_layout(
        title='Evolución Poblacional: Histórico y Proyecciones (1985-2050)',
        title_x=0.5,
        xaxis_title="Año",
        yaxis_title="Población Total",
        hovermode='x unified',
        template='plotly_white',
        height=600,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    return fig

def plot_error_analysis(comparison):
    """Gráfico de análisis de errores"""
    fig = px.bar(
        comparison,
        x='AÑO',
        y='ERROR_PORCENTUAL',
        title='Error Porcentual del Modelo por Año',
        labels={'AÑO': 'Año', 'ERROR_PORCENTUAL': 'Error Porcentual (%)'},
        color='ERROR_PORCENTUAL',
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        title_x=0.5,
        template='plotly_white',
        height=400
    )
    
    return fig

def create_metrics_cards(stats, metrics):
    """Crea tarjetas de métricas principales"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Población Máxima",
            value=f"{stats['max']:,.0f}",
            delta=f"Año {stats['max_year']:.0f}"
        )
    
    with col2:
        st.metric(
            label="R² del Modelo",
            value=f"{metrics['r2']:.4f}",
            delta="Bondad de ajuste"
        )
    
    with col3:
        st.metric(
            label="Error Promedio",
            value=f"{metrics['mae']:,.0f}",
            delta="habitantes"
        )
    
    with col4:
        st.metric(
            label="Crecimiento Anual",
            value=f"{(stats['max'] - stats['min']) / (stats['max_year'] - stats['min_year']):,.0f}",
            delta="hab/año promedio"
        )

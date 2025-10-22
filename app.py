# -*- coding: utf-8 -*-
"""
Aplicación Streamlit - Predicción de Crecimiento Poblacional en Antioquia
"""

import streamlit as st
import pandas as pd
from data_processor import process_data, get_statistics
from model import run_complete_analysis
from visualization import (
    plot_historical_population, 
    plot_real_vs_predicted, 
    plot_future_predictions,
    plot_error_analysis,
    create_metrics_cards
)

# Configuración de la página
st.set_page_config(
    page_title="Predicción Poblacional Antioquia",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Título principal
    st.markdown('<h1 class="main-header">🏘️ Predicción de Crecimiento Poblacional</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Análisis predictivo basado en datos históricos de Antioquia (1985-2050)</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("⚙️ Configuración")
    st.sidebar.markdown("---")
    
    # Cargar y procesar datos
    with st.spinner("Cargando y procesando datos..."):
        df_filtered = process_data()
        
        if df_filtered is None:
            st.error("Error al cargar los datos. Verifica que los archivos Excel estén en la carpeta 'data/'")
            return
        
        stats, df_stats = get_statistics(df_filtered)
        analysis_results = run_complete_analysis(df_filtered)
    
    # Opciones de visualización
    st.sidebar.subheader("📊 Visualizaciones")
    show_historical = st.sidebar.checkbox("Evolución Histórica", value=True)
    show_comparison = st.sidebar.checkbox("Real vs Predicción", value=True)
    show_future = st.sidebar.checkbox("Proyecciones Futuras", value=True)
    show_errors = st.sidebar.checkbox("Análisis de Errores", value=False)
    
    # Parámetros del modelo
    st.sidebar.subheader("🔧 Parámetros del Modelo")
    train_cutoff = st.sidebar.slider("Año de corte entrenamiento", 2010, 2020, 2015)
    future_end = st.sidebar.slider("Proyección hasta", 2030, 2060, 2050)
    
    # Métricas principales
    st.subheader("📈 Métricas Principales")
    create_metrics_cards(stats, analysis_results['metrics'])
    
    st.markdown("---")
    
    # Información del dataset
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Información del Dataset")
        st.write(f"**Total de registros:** {len(df_filtered):,}")
        st.write(f"**Rango temporal:** {df_stats['AÑO'].min():.0f} - {df_stats['AÑO'].max():.0f}")
        st.write(f"**Población promedio:** {stats['mean']:,.0f} habitantes")
        st.write(f"**Desviación estándar:** {stats['std']:,.0f}")
    
    with col2:
        st.subheader("🎯 Métricas del Modelo")
        metrics = analysis_results['metrics']
        st.write(f"**R² (Bondad de ajuste):** {metrics['r2']:.4f}")
        st.write(f"**Error Absoluto Medio:** {metrics['mae']:,.0f} habitantes")
        st.write(f"**Error Cuadrático Medio:** {metrics['rmse']:,.0f} habitantes")
        
        params = analysis_results['model_params']
        st.write(f"**Crecimiento anual estimado:** {params['pendiente']:,.0f} hab/año")
    
    # Visualizaciones
    st.markdown("---")
    
    if show_historical:
        st.subheader("📊 Evolución Histórica de la Población")
        fig_historical = plot_historical_population(df_stats)
        st.plotly_chart(fig_historical, use_container_width=True)
    
    if show_comparison:
        st.subheader("🔍 Comparación: Real vs Predicción (2016-2025)")
        fig_comparison = plot_real_vs_predicted(analysis_results['comparison'])
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Tabla de comparación
        st.subheader("📋 Tabla de Comparación Detallada")
        comparison_display = analysis_results['comparison'].copy()
        comparison_display['TOTAL'] = comparison_display['TOTAL'].apply(lambda x: f"{x:,.0f}")
        comparison_display['PREDICCION'] = comparison_display['PREDICCION'].apply(lambda x: f"{x:,.0f}")
        comparison_display['ERROR_ABSOLUTO'] = comparison_display['ERROR_ABSOLUTO'].apply(lambda x: f"{x:,.0f}")
        comparison_display['ERROR_PORCENTUAL'] = comparison_display['ERROR_PORCENTUAL'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(
            comparison_display[['AÑO', 'TOTAL', 'PREDICCION', 'ERROR_ABSOLUTO', 'ERROR_PORCENTUAL']],
            use_container_width=True
        )
    
    if show_future:
        st.subheader("🔮 Proyecciones Futuras (2026-2050)")
        fig_future = plot_future_predictions(analysis_results['df_model'], analysis_results['future_predictions'])
        st.plotly_chart(fig_future, use_container_width=True)
        
        # Tabla de proyecciones
        st.subheader("📋 Tabla de Proyecciones")
        future_display = analysis_results['future_predictions'].copy()
        future_display['PREDICCION_TOTAL'] = future_display['PREDICCION_TOTAL'].apply(lambda x: f"{x:,.0f}")
        
        # Mostrar por quinquenios
        quinquenios = future_display[future_display['AÑO'] % 5 == 0]
        st.dataframe(quinquenios, use_container_width=True)
    
    if show_errors:
        st.subheader("❌ Análisis de Errores del Modelo")
        fig_errors = plot_error_analysis(analysis_results['comparison'])
        st.plotly_chart(fig_errors, use_container_width=True)
    
    # Información adicional
    st.markdown("---")
    st.subheader("ℹ️ Información del Proyecto")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **📊 Fuente de Datos**
        - DANE (Departamento Administrativo Nacional de Estadística)
        - Proyecciones poblacionales oficiales
        - Período: 1985-2050
        """)
    
    with col2:
        st.info("""
        **🤖 Metodología**
        - Regresión lineal simple
        - Validación temporal (train/test)
        - Métricas: MAE, MSE, R²
        """)
    
    with col3:
        st.info("""
        **🎯 Aplicaciones**
        - Planificación urbana
        - Políticas públicas
        - Proyección de servicios
        """)

if __name__ == "__main__":
    main()

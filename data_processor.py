# -*- coding: utf-8 -*-
"""
Módulo de procesamiento de datos para predicción poblacional Antioquia
"""

import pandas as pd
import streamlit as st
import os

@st.cache_data
def load_excel_files():
    """Carga los 4 archivos Excel con datos poblacionales"""
    try:
        # Rutas de los archivos
        files = {
            'df4': ('data/PPED-AreaDep-2018-2050_VP.xlsx', 'PobDepartamentalxÁrea', 7),
            'df3': ('data/DCD-area-proypoblacion-dep-2005-2017_VP.xlsx', None, 11),
            'df2': ('data/DCD-areaproypoblacion-dep-1993-2004.xlsx', None, 11),
            'df1': ('data/DCD-area-proypoblacion-dep-1985-1992.xlsx', None, 11)
        }
        
        dataframes = {}
        for key, (path, sheet, header) in files.items():
            if key == 'df4':
                dataframes[key] = pd.read_excel(path, sheet_name=sheet, header=[header])
            else:
                dataframes[key] = pd.read_excel(path, header=header)
        
        return dataframes
    except Exception as e:
        st.error(f"Error cargando archivos: {str(e)}")
        return None

def estandarizar_df123(df):
    """Estandariza estructura para df1, df2, df3"""
    df_std = df.copy()
    df_std.columns = ['SIGLA_REGION', 'TERRITORIO', 'AÑO', 'AREA_GEOGRAFICA', 'TOTAL']
    return df_std

def estandarizar_df4(df):
    """Estandariza estructura para df4 (diferente)"""
    df_std = df.copy()
    df_std.columns = ['SIGLA_REGION', 'TERRITORIO', 'AÑO', 'AREA_GEOGRAFICA', 'TOTAL']
    # Transformación específica para Antioquia y Urabá
    df_std['TERRITORIO'] = df_std['TERRITORIO'].str.replace(
        r'Antioquia.*Urabá', 'Antioquia', case=False, regex=True
    )
    return df_std

@st.cache_data
def process_data():
    """Procesa y limpia todos los datos"""
    dataframes = load_excel_files()
    if dataframes is None:
        return None
    
    # Aplicar estandarización
    df1_std = estandarizar_df123(dataframes['df1'])
    df2_std = estandarizar_df123(dataframes['df2'])
    df3_std = estandarizar_df123(dataframes['df3'])
    df4_std = estandarizar_df4(dataframes['df4'])
    
    # Limpiar DataFrames (eliminar nulos)
    dfs_clean = [df.dropna() for df in [df1_std, df2_std, df3_std, df4_std]]
    
    # Unir todos los DataFrames
    df_all = pd.concat(dfs_clean, ignore_index=True)
    
    # Filtrar por territorio y área geográfica
    df_filtered = df_all[
        (df_all['TERRITORIO'] == 'Antioquia') & 
        (df_all['AREA_GEOGRAFICA'] == 'Total')
    ]
    
    return df_filtered

def get_statistics(df):
    """Calcula estadísticas básicas de los datos"""
    df_stats = df.groupby('AÑO', as_index=False)['TOTAL'].sum()
    
    stats = {
        'max': df_stats['TOTAL'].max(),
        'min': df_stats['TOTAL'].min(),
        'mean': df_stats['TOTAL'].mean(),
        'median': df_stats['TOTAL'].median(),
        'std': df_stats['TOTAL'].std()
    }
    
    # Años con valores extremos
    max_year = df_stats.loc[df_stats['TOTAL'].idxmax(), 'AÑO']
    min_year = df_stats.loc[df_stats['TOTAL'].idxmin(), 'AÑO']
    
    stats['max_year'] = max_year
    stats['min_year'] = min_year
    
    return stats, df_stats

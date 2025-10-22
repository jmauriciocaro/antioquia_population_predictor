# -*- coding: utf-8 -*-
"""
Módulo del modelo de machine learning para predicción poblacional
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import streamlit as st

class PopulationPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
        
    def prepare_data(self, df_filtered, train_cutoff=2015):
        """Prepara los datos para entrenamiento y prueba"""
        df_model = df_filtered.groupby('AÑO', as_index=False)['TOTAL'].sum()
        
        # División temporal
        train_df = df_model[df_model['AÑO'] <= train_cutoff]
        test_df = df_model[(df_model['AÑO'] > train_cutoff) & (df_model['AÑO'] <= 2025)]
        
        return train_df, test_df, df_model
    
    def train_model(self, train_df):
        """Entrena el modelo de regresión lineal"""
        X_train = train_df[['AÑO']]
        y_train = train_df['TOTAL']
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        return X_train, y_train
    
    def evaluate_model(self, test_df):
        """Evalúa el modelo con datos de prueba"""
        if not self.is_trained:
            raise ValueError("El modelo debe ser entrenado primero")
            
        X_test = test_df[['AÑO']]
        y_test = test_df['TOTAL']
        y_pred = self.model.predict(X_test)
        
        # Métricas
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # DataFrame de comparación
        comparison = test_df.copy()
        comparison['PREDICCION'] = y_pred
        comparison['ERROR_ABSOLUTO'] = abs(comparison['TOTAL'] - comparison['PREDICCION'])
        comparison['ERROR_PORCENTUAL'] = (comparison['ERROR_ABSOLUTO'] / comparison['TOTAL']) * 100
        
        metrics = {
            'mae': mae,
            'mse': mse,
            'r2': r2,
            'rmse': np.sqrt(mse)
        }
        
        return metrics, comparison
    
    def predict_future(self, start_year=2026, end_year=2050):
        """Realiza predicciones futuras"""
        if not self.is_trained:
            raise ValueError("El modelo debe ser entrenado primero")
            
        future_years = pd.DataFrame({'AÑO': range(start_year, end_year + 1)})
        future_years['PREDICCION_TOTAL'] = self.model.predict(future_years[['AÑO']])
        
        return future_years
    
    def get_model_params(self):
        """Obtiene parámetros del modelo"""
        if not self.is_trained:
            return None
            
        return {
            'pendiente': self.model.coef_[0],
            'intercepto': self.model.intercept_
        }

@st.cache_data
def run_complete_analysis(df_filtered):
    """Ejecuta análisis completo con caché"""
    predictor = PopulationPredictor()
    
    # Preparar datos
    train_df, test_df, df_model = predictor.prepare_data(df_filtered)
    
    # Entrenar modelo
    predictor.train_model(train_df)
    
    # Evaluar modelo
    metrics, comparison = predictor.evaluate_model(test_df)
    
    # Predicciones futuras
    future_predictions = predictor.predict_future()
    
    # Parámetros del modelo
    model_params = predictor.get_model_params()
    
    return {
        'train_df': train_df,
        'test_df': test_df,
        'df_model': df_model,
        'metrics': metrics,
        'comparison': comparison,
        'future_predictions': future_predictions,
        'model_params': model_params,
        'predictor': predictor
    }

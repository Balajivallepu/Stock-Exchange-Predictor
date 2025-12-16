"""
Stock Price Prediction using Machine Learning
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

class StockPredictor:
    """Machine Learning based stock price predictor"""
    
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def prepare_data(self, df, lookback=30):
        """
        Prepare data for prediction
        
        Args:
            df: DataFrame with stock data
            lookback: Number of days to look back for features
        
        Returns:
            X, y: Features and target arrays
        """
        if df is None or len(df) < lookback + 1:
            return None, None
        
        # Create features from historical data
        features = []
        targets = []
        
        data = df['Close'].values
        
        for i in range(lookback, len(data)):
            features.append(data[i-lookback:i])
            targets.append(data[i])
        
        return np.array(features), np.array(targets)
    
    def train_model(self, df, lookback=30):
        """Train prediction model"""
        X, y = self.prepare_data(df, lookback)
        
        if X is None or len(X) < 20:
            return False
        
        # Split into train and test
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Calculate accuracy
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        return True
    
    def predict_next_days(self, df, days=7, lookback=30):
        """
        Predict stock prices for next N days
        
        Args:
            df: Historical stock data
            days: Number of days to predict
            lookback: Number of days to use for prediction
        
        Returns:
            Dictionary with predictions
        """
        if df is None or len(df) < lookback:
            return None
        
        # Train model
        success = self.train_model(df, lookback)
        if not success:
            return None
        
        # Get last 'lookback' days
        last_data = df['Close'].values[-lookback:]
        predictions = []
        dates = []
        
        current_data = last_data.copy()
        last_date = df.index[-1]
        
        for i in range(days):
            # Predict next day
            pred = self.model.predict(current_data.reshape(1, -1))[0]
            predictions.append(pred)
            
            # Update data for next prediction
            current_data = np.append(current_data[1:], pred)
            
            # Calculate next business day
            next_date = last_date + timedelta(days=i+1)
            # Skip weekends
            while next_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                next_date += timedelta(days=1)
            dates.append(next_date)
        
        return {
            'dates': dates,
            'predictions': predictions,
            'current_price': df['Close'].iloc[-1],
            'predicted_change': ((predictions[-1] - df['Close'].iloc[-1]) / df['Close'].iloc[-1]) * 100
        }
    
    def get_prediction_confidence(self, df):
        """Calculate confidence level of predictions"""
        if df is None or len(df) < 50:
            return 0
        
        # Use volatility and data quality to determine confidence
        returns = df['Close'].pct_change().dropna()
        volatility = returns.std()
        
        # Lower volatility = higher confidence
        if volatility < 0.02:
            return 85
        elif volatility < 0.03:
            return 70
        elif volatility < 0.05:
            return 55
        else:
            return 40

def simple_linear_prediction(df, days=7):
    """Simple linear regression prediction (fallback method)"""
    if df is None or len(df) < 30:
        return None
    
    # Prepare data
    df_recent = df.tail(60).copy()
    df_recent['Days'] = range(len(df_recent))
    
    X = df_recent['Days'].values.reshape(-1, 1)
    y = df_recent['Close'].values
    
    # Train simple linear model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict future
    future_days = np.array(range(len(df_recent), len(df_recent) + days)).reshape(-1, 1)
    predictions = model.predict(future_days)
    
    last_date = df.index[-1]
    dates = []
    for i in range(days):
        next_date = last_date + timedelta(days=i+1)
        while next_date.weekday() >= 5:
            next_date += timedelta(days=1)
        dates.append(next_date)
    
    return {
        'dates': dates,
        'predictions': predictions.tolist(),
        'current_price': df['Close'].iloc[-1],
        'predicted_change': ((predictions[-1] - df['Close'].iloc[-1]) / df['Close'].iloc[-1]) * 100
    }

def calculate_support_resistance(df):
    """Calculate support and resistance levels"""
    if df is None or len(df) < 20:
        return None
    
    recent = df.tail(50)
    
    # Simple support/resistance based on recent highs/lows
    resistance = recent['High'].max()
    support = recent['Low'].min()
    
    current_price = df['Close'].iloc[-1]
    
    return {
        'support': support,
        'resistance': resistance,
        'current': current_price,
        'distance_to_support': ((current_price - support) / current_price) * 100,
        'distance_to_resistance': ((resistance - current_price) / current_price) * 100
    }
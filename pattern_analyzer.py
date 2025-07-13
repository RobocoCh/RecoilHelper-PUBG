"""
Recoil pattern analyzer and machine learning module
Educational purposes only
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import pickle
import os
from typing import List, Tuple, Dict
import json

class PatternAnalyzer:
    """Analyze and learn recoil patterns"""
    
    def __init__(self):
        self.patterns_db = {}
        self.scaler = StandardScaler()
        self.clustering_model = DBSCAN(eps=0.5, min_samples=5)
        self.pattern_cache_file = "patterns_cache.pkl"
        self.load_patterns()
    
    def record_pattern(self, weapon: str, shots: List[Tuple[float, float]]):
        """Record shooting pattern for analysis"""
        if weapon not in self.patterns_db:
            self.patterns_db[weapon] = []
        
        # Normalize pattern
        normalized = self._normalize_pattern(shots)
        self.patterns_db[weapon].append(normalized)
        
        # Auto-save every 10 patterns
        if len(self.patterns_db[weapon]) % 10 == 0:
            self.save_patterns()
    
    def _normalize_pattern(self, pattern: List[Tuple[float, float]]) -> np.ndarray:
        """Normalize recoil pattern"""
        if len(pattern) < 2:
            return np.array(pattern)
        
        # Convert to numpy array
        arr = np.array(pattern)
        
        # Center around origin
        arr -= arr[0]
        
        # Scale to unit variance
        if arr.std() > 0:
            arr = self.scaler.fit_transform(arr)
        
        return arr
    
    def analyze_weapon_pattern(self, weapon: str) -> Dict:
        """Analyze patterns for specific weapon"""
        if weapon not in self.patterns_db or len(self.patterns_db[weapon]) < 5:
            return {"status": "insufficient_data"}
        
        patterns = np.vstack(self.patterns_db[weapon])
        
        # Cluster analysis
        clusters = self.clustering_model.fit_predict(patterns)
        
        # Find dominant pattern
        unique, counts = np.unique(clusters, return_counts=True)
        dominant_cluster = unique[np.argmax(counts)]
        
        # Calculate average pattern
        dominant_patterns = patterns[clusters == dominant_cluster]
        avg_pattern = np.mean(dominant_patterns, axis=0)
        
        # Calculate variance
        pattern_variance = np.var(dominant_patterns, axis=0)
        
        return {
            "status": "analyzed",
            "average_pattern": avg_pattern.tolist(),
            "variance": pattern_variance.tolist(),
            "confidence": float(np.max(counts) / len(patterns)),
            "total_samples": len(patterns)
        }
    
    def predict_next_shots(self, weapon: str, current_shots: List[Tuple[float, float]], 
                          num_predictions: int = 5) -> List[Tuple[float, float]]:
        """Predict next shots based on learned patterns"""
        analysis = self.analyze_weapon_pattern(weapon)
        
        if analysis["status"] != "analyzed":
            # Return simple linear prediction
            return self._linear_prediction(current_shots, num_predictions)
        
        avg_pattern = np.array(analysis["average_pattern"])
        variance = np.array(analysis["variance"])
        
        predictions = []
        start_idx = len(current_shots)
        
        for i in range(num_predictions):
            if start_idx + i < len(avg_pattern):
                # Use learned pattern
                pred = avg_pattern[start_idx + i]
                # Add controlled randomness based on variance
                noise = np.random.normal(0, np.sqrt(variance[start_idx + i]) * 0.1)
                predictions.append(tuple(pred + noise))
            else:
                # Extrapolate
                predictions.extend(self._linear_prediction(
                    predictions[-3:] if len(predictions) >= 3 else current_shots[-3:],
                    num_predictions - i
                ))
                break
        
        return predictions
    
    def _linear_prediction(self, recent_shots: List[Tuple[float, float]], 
                          num_predictions: int) -> List[Tuple[float, float]]:
        """Simple linear prediction"""
        if len(recent_shots) < 2:
            return [(0, 0)] * num_predictions
        
        # Calculate trend
        x_vals = [s[0] for s in recent_shots]
        y_vals = [s[1] for s in recent_shots]
        
        x_trend = (x_vals[-1] - x_vals[0]) / len(x_vals)
        y_trend = (y_vals[-1] - y_vals[0]) / len(y_vals)
        
        predictions = []
        last_x, last_y = recent_shots[-1]
        
        for i in range(1, num_predictions + 1):
            pred_x = last_x + x_trend * i
            pred_y = last_y + y_trend * i
            predictions.append((pred_x, pred_y))
        
        return predictions
    
    def save_patterns(self):
        """Save patterns to file"""
        try:
            with open(self.pattern_cache_file, 'wb') as f:
                pickle.dump({
                    'patterns': self.patterns_db,
                    'scaler': self.scaler,
                    'clustering': self.clustering_model
                }, f)
        except Exception as e:
            print(f"Failed to save patterns: {e}")
    
    def load_patterns(self):
        """Load patterns from file"""
        if os.path.exists(self.pattern_cache_file):
            try:
                with open(self.pattern_cache_file, 'rb') as f:
                    data = pickle.load(f)
                    self.patterns_db = data.get('patterns', {})
                    self.scaler = data.get('scaler', self.scaler)
                    self.clustering_model = data.get('clustering', self.clustering_model)
            except Exception as e:
                print(f"Failed to load patterns: {e}")

class AdaptiveCompensation:
    """Adaptive compensation based on real-time analysis"""
    
    def __init__(self, analyzer: PatternAnalyzer):
        self.analyzer = analyzer
        self.adaptation_rate = 0.1
        self.current_compensation = {}
        
    def adapt_compensation(self, weapon: str, actual_movement: Tuple[float, float],
                         expected_movement: Tuple[float, float]):
        """Adapt compensation based on actual vs expected movement"""
        if weapon not in self.current_compensation:
            self.current_compensation[weapon] = {'x': 1.0, 'y': 1.0}
        
        # Calculate error
        error_x = actual_movement[0] - expected_movement[0]
        error_y = actual_movement[1] - expected_movement[1]
        
        # Adapt multipliers
        self.current_compensation[weapon]['x'] += error_x * self.adaptation_rate
        self.current_compensation[weapon]['y'] += error_y * self.adaptation_rate
        
        # Clamp values
        self.current_compensation[weapon]['x'] = np.clip(
            self.current_compensation[weapon]['x'], 0.5, 2.0
        )
        self.current_compensation[weapon]['y'] = np.clip(
            self.current_compensation[weapon]['y'], 0.5, 2.0
        )
    
    def get_adapted_compensation(self, weapon: str, base_compensation: Tuple[float, float]) -> Tuple[float, float]:
        """Get adapted compensation values"""
        if weapon not in self.current_compensation:
            return base_compensation
        
        adapted_x = base_compensation[0] * self.current_compensation[weapon]['x']
        adapted_y = base_compensation[1] * self.current_compensation[weapon]['y']
        
        return (adapted_x, adapted_y)
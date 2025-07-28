import numpy as np
from typing import List, Tuple, Optional, Dict
import json
from dataclasses import dataclass

@dataclass
class NeuralConfig:
    input_size: int
    hidden_sizes: List[int]
    output_size: int
    learning_rate: float = 0.01
    activation: str = 'relu'

class NeuralLayer:
    def __init__(self, input_size: int, output_size: int):
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.biases = np.zeros((1, output_size))
        self.input_cache = None
        self.output_cache = None
        self.weight_gradients = None
        self.bias_gradients = None

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        self.input_cache = input_data
        self.output_cache = np.dot(input_data, self.weights) + self.biases
        return self.output_cache

    def backward(self, gradient: np.ndarray) -> np.ndarray:
        self.weight_gradients = np.dot(self.input_cache.T, gradient)
        self.bias_gradients = np.sum(gradient, axis=0, keepdims=True)
        return np.dot(gradient, self.weights.T)

    def update(self, learning_rate: float):
        self.weights -= learning_rate * self.weight_gradients
        self.biases -= learning_rate * self.bias_gradients

class AdvancedNeuralNetwork:
    def __init__(self, config: NeuralConfig):
        self.config = config
        self.layers = []
        self.setup_layers()

    def setup_layers(self):
        layer_sizes = [self.config.input_size] + \
                     self.config.hidden_sizes + \
                     [self.config.output_size]
        
        for i in range(len(layer_sizes) - 1):
            self.layers.append(NeuralLayer(layer_sizes[i], layer_sizes[i + 1]))

    def activate(self, x: np.ndarray) -> np.ndarray:
        if self.config.activation == 'relu':
            return np.maximum(0, x)
        elif self.config.activation == 'sigmoid':
            return 1 / (1 + np.exp(-x))
        return x

    def activate_derivative(self, x: np.ndarray) -> np.ndarray:
        if self.config.activation == 'relu':
            return (x > 0).astype(float)
        elif self.config.activation == 'sigmoid':
            return x * (1 - x)
        return np.ones_like(x)

    def forward(self, input_data: np.ndarray) -> np.ndarray:
        current_output = input_data
        for layer in self.layers:
            current_output = self.activate(layer.forward(current_output))
        return current_output

    def backward(self, gradient: np.ndarray):
        current_gradient = gradient
        for layer in reversed(self.layers):
            current_gradient = layer.backward(current_gradient)
            current_gradient = current_gradient * \
                self.activate_derivative(layer.output_cache)

    def update(self):
        for layer in self.layers:
            layer.update(self.config.learning_rate)

    def train(self, 
             input_data: np.ndarray, 
             target_data: np.ndarray, 
             epochs: int,
             batch_size: int = 32) -> List[float]:
        losses = []
        
        for epoch in range(epochs):
            epoch_loss = 0
            
            # Mini-batch training
            for i in range(0, len(input_data), batch_size):
                batch_input = input_data[i:i + batch_size]
                batch_target = target_data[i:i + batch_size]
                
                # Forward pass
                predictions = self.forward(batch_input)
                
                # Calculate loss
                loss = np.mean((predictions - batch_target) ** 2)
                epoch_loss += loss
                
                # Backward pass
                gradient = 2 * (predictions - batch_target) / batch_size
                self.backward(gradient)
                
                # Update weights
                self.update()
            
            losses.append(epoch_loss / (len(input_data) / batch_size))
            
        return losses

class EmotionRecognizer:
    def __init__(self):
        self.config = NeuralConfig(
            input_size=128,  # Feature vector size
            hidden_sizes=[64, 32],
            output_size=4,   # Number of emotions
            learning_rate=0.01,
            activation='relu'
        )
        self.model = AdvancedNeuralNetwork(self.config)
        self.emotion_map = ['neutral', 'happy', 'sad', 'surprised']

    def extract_features(self, text: str) -> np.ndarray:
        # Simple feature extraction - would be replaced with more sophisticated embedding
        features = np.zeros(128)
        for i, char in enumerate(text[:128]):
            features[i] = ord(char) / 255  # Normalize
        return features.reshape(1, -1)

    def predict_emotion(self, text: str) -> Tuple[str, float]:
        features = self.extract_features(text)
        prediction = self.model.forward(features)
        emotion_idx = np.argmax(prediction)
        confidence = float(prediction[0][emotion_idx])
        return self.emotion_map[emotion_idx], confidence

class FaceAnimator:
    def __init__(self):
        self.base_expressions = self._load_expressions()
        self.transition_state = None
        self.current_emotion = 'neutral'

    def _load_expressions(self) -> Dict[str, Dict]:
        return {
            'neutral': {
                'mouth_curve': 0,
                'eye_openness': 1,
                'eyebrow_angle': 0
            },
            'happy': {
                'mouth_curve': 0.5,
                'eye_openness': 0.8,
                'eyebrow_angle': 0.2
            },
            'sad': {
                'mouth_curve': -0.3,
                'eye_openness': 0.7,
                'eyebrow_angle': -0.2
            },
            'surprised': {
                'mouth_curve': 0,
                'eye_openness': 1.2,
                'eyebrow_angle': 0.4
            }
        }

    def get_expression_params(self, 
                            emotion: str, 
                            intensity: float = 1.0,
                            speaking: bool = False) -> Dict[str, float]:
        base = self.base_expressions[emotion]
        
        # Apply intensity
        params = {
            k: v * intensity for k, v in base.items()
        }
        
        # Modify for speaking state
        if speaking:
            params['mouth_curve'] *= np.sin(time.time() * 10) * 0.3
            params['mouth_openness'] = 0.5 + np.sin(time.time() * 15) * 0.2
        
        return params

    def interpolate_expression(self, 
                             start_emotion: str,
                             end_emotion: str,
                             progress: float) -> Dict[str, float]:
        start_params = self.base_expressions[start_emotion]
        end_params = self.base_expressions[end_emotion]
        
        return {
            k: start_params[k] + (end_params[k] - start_params[k]) * progress
            for k in start_params.keys()
        }

class SecurityManager:
    def __init__(self):
        self.hashing_salt = os.urandom(16)
        self.active_sessions = {}
        self.rate_limits = defaultdict(lambda: {'count': 0, 'reset_time': 0})
        
    def generate_token(self, user_id: str) -> str:
        """Generate secure session token"""
        timestamp = int(time.time())
        token_data = f"{user_id}:{timestamp}"
        token_hash = hashlib.sha256(
            token_data.encode() + self.hashing_salt
        ).hexdigest()
        
        self.active_sessions[token_hash] = {
            'user_id': user_id,
            'created_at': timestamp,
            'expires_at': timestamp + 3600  # 1 hour expiration
        }
        
        return token_hash

    def validate_token(self, token: str) -> Optional[str]:
        """Validate session token and return user_id if valid"""
        session = self.active_sessions.get(token)
        if not session:
            return None
            
        if time.time() > session['expires_at']:
            del self.active_sessions[token]
            return None
            
        return session['user_id']

    def check_rate_limit(self, user_id: str, limit: int = 100, window: int = 3600) -> bool:
        """Check if user has exceeded rate limit"""
        current_time = time.time()
        user_limits = self.rate_limits[user_id]
        
        # Reset if window has passed
        if current_time > user_limits['reset_time']:
            user_limits['count'] = 0
            user_limits['reset_time'] = current_time + window
        
        # Check limit
        if user_limits['count'] >= limit:
            return False
            
        user_limits['count'] += 1
        return True

if __name__ == "__main__":
    # Initialize components
    emotion_recognizer = EmotionRecognizer()
    face_animator = FaceAnimator()
    security_manager = SecurityManager()
    
    # Example usage
    text = "I'm so happy to see this working!"
    
    # Recognize emotion
    emotion, confidence = emotion_recognizer.predict_emotion(text)
    print(f"Detected emotion: {emotion} (confidence: {confidence:.2f})")
    
    # Get animation parameters
    expression_params = face_animator.get_expression_params(
        emotion=emotion,
        intensity=confidence,
        speaking=True
    )
    print(f"Animation parameters: {json.dumps(expression_params, indent=2)}")

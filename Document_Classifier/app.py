from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from controllers.train_controller import train_bp
from controllers.predict_controller import predict_bp
from controllers.ocr_controller import ocr_bp

app = Flask(__name__)
CORS(app)
Swagger(app)

app.register_blueprint(train_bp, url_prefix='/api/train')
app.register_blueprint(predict_bp, url_prefix='/api/predict')
app.register_blueprint(ocr_bp, url_prefix='/api/ocr')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
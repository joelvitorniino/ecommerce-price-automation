from flask import Blueprint, jsonify, current_app
from app.services.price_automation import start_automation, stop_automation, get_automation_status

automation_bp = Blueprint('automation', __name__, url_prefix='/automation')

@automation_bp.route('/start', methods=['POST'])
def start():
    """
    Inicia a automação de preços.
    ---
    tags:
      - Automação
    responses:
      200:
        description: Automação iniciada com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Automation started.
      400:
        description: A automação já está em execução.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Automation is already running.
    """
    if start_automation(current_app._get_current_object()):
        return jsonify({'message': 'Automation started.'}), 200
    else:
        return jsonify({'message': 'Automation is already running.'}), 400

@automation_bp.route('/stop', methods=['POST'])
def stop():
    """
    Para a automação de preços.
    ---
    tags:
      - Automação
    responses:
      200:
        description: Automação parada com sucesso.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Automation stopped.
      400:
        description: A automação não estava em execução.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Automation was not running.
    """
    if stop_automation():
        return jsonify({'message': 'Automation stopped.'}), 200
    else:
        return jsonify({'message': 'Automation was not running.'}), 400

@automation_bp.route('/status', methods=['GET'])
def status():
    """
    Retorna o status da automação de preços.
    ---
    tags:
      - Automação
    responses:
      200:
        description: Status da automação.
        schema:
          type: object
          properties:
            automation_active:
              type: boolean
              example: true
    """
    status = get_automation_status()
    return jsonify({'automation_active': status}), 200

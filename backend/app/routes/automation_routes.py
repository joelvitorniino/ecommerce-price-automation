from flask import Blueprint, jsonify
from app.services.price_automation import price_automation

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
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Automation started.
      400:
        description: A automação já está em execução.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Automation is already running.
      500:
        description: Erro ao tentar iniciar a automação.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                details:
                  type: string
    """
    try:
        if price_automation.start():
            return jsonify({'message': 'Automation started.'}), 200
        else:
            return jsonify({'message': 'Automation is already running.'}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to start automation', 'details': str(e)}), 500

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
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Automation stopped.
      400:
        description: A automação não estava em execução.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Automation was not running.
      500:
        description: Erro ao tentar parar a automação.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                details:
                  type: string
    """
    try:
        if price_automation.stop():
            return jsonify({'message': 'Automation stopped.'}), 200
        else:
            return jsonify({'message': 'Automation was not running.'}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to stop automation', 'details': str(e)}), 500

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
        content:
          application/json:
            schema:
              type: object
              properties:
                automation_active:
                  type: boolean
                  example: true
      500:
        description: Erro ao tentar obter o status da automação.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                details:
                  type: string
    """
    try:
        status = price_automation.is_running()
        return jsonify({'automation_active': status}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to get automation status', 'details': str(e)}), 500

from flask import Blueprint, jsonify, make_response, current_app
from flask_caching import Cache
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

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
        logger.debug("Attempting to start price automation")
        if current_app.price_automation.start():
            response = make_response(jsonify({'message': 'Automation started.'}), 200)
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            logger.info("Price automation started successfully")
            return response
        else:
            response = make_response(jsonify({'message': 'Automation is already running.'}), 400)
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            logger.warning("Price automation already running")
            return response
    except Exception as e:
        logger.error(f"Failed to start automation: {str(e)}")
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
        logger.debug("Attempting to stop price automation")
        if current_app.price_automation.stop():
            response = make_response(jsonify({'message': 'Automation stopped.'}), 200)
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            logger.info("Price automation stopped successfully")
            return response
        else:
            response = make_response(jsonify({'message': 'Automation was not running.'}), 400)
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            logger.warning("Price automation was not running")
            return response
    except Exception as e:
        logger.error(f"Failed to stop automation: {str(e)}")
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
                last_update:
                  type: string
                  example: "2025-06-01T22:12:34.123Z"
                update_count:
                  type: integer
                  example: 10
                error_count:
                  type: integer
                  example: 0
                interval:
                  type: number
                  example: 10
                price_range:
                  type: object
                  properties:
                    min_factor:
                      type: number
                      example: 0.8
                    max_factor:
                      type: number
                      example: 1.2
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
        logger.debug("Fetching price automation status")
        status = current_app.price_automation.get_status()
        response = make_response(jsonify(status), 200)
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        logger.info(f"Automation status: {status}")
        return response
    except Exception as e:
        logger.error(f"Failed to get automation status: {str(e)}")
        return jsonify({'error': 'Failed to get automation status', 'details': str(e)}), 500
"""
Start Mobile API Server - Run this to start the mobile API server
"""

from loguru import logger
from src.api.mobile_api import get_mobile_api


def start_mobile_api(host='0.0.0.0', port=5000, debug=False, api_key=None):
    """
    Start the mobile API server
    
    Args:
        host: Host to bind to (default: 0.0.0.0 for all interfaces)
        port: Port to bind to (default: 5000)
        debug: Enable debug mode (default: False)
        api_key: Optional API key for authentication (default: None)
    """
    try:
        api = get_mobile_api()
        logger.info("Starting Mobile Companion API Server...")
        logger.info(f"API will be available at: http://{host}:{port}/api/mobile")
        if api_key:
            logger.info("API key authentication enabled")
        logger.info("Endpoints:")
        logger.info("  GET  /api/mobile/health - Health check")
        logger.info("  GET  /api/mobile/orders - Get orders")
        logger.info("  GET  /api/mobile/orders/<id> - Get order details")
        logger.info("  POST /api/mobile/orders/create - Create new order")
        logger.info("  PUT  /api/mobile/orders/<id>/status - Update order status")
        logger.info("  GET  /api/mobile/products - Get products")
        logger.info("  GET  /api/mobile/dashboard - Get dashboard stats")
        logger.info("  GET  /api/mobile/inventory - Get inventory")
        logger.info("  GET  /api/mobile/inventory/alerts - Get inventory alerts")
        logger.info("  PUT  /api/mobile/inventory/<id>/update - Update inventory")
        logger.info("  GET  /api/mobile/staff - Get staff")
        logger.info("  GET  /api/mobile/staff/shifts - Get staff shifts")
        logger.info("  GET  /api/mobile/staff/attendance - Get attendance")
        logger.info("  POST /api/mobile/staff/clock-in - Clock in")
        logger.info("  POST /api/mobile/staff/clock-out - Clock out")
        logger.info("  GET  /api/mobile/customers - Get customers")
        logger.info("  POST /api/mobile/customers - Create customer")
        logger.info("  GET  /api/mobile/locations - Get locations")
        api.run(host=host, port=port, debug=debug, api_key=api_key)
    except Exception as e:
        logger.error(f"Error starting mobile API: {e}")
        raise


if __name__ == "__main__":
    start_mobile_api(debug=True)


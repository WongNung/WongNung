from django.shortcuts import render
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def error_404_view(request, exception=None):
    # Get the username if available
    username = request.user.username if request.user.is_authenticated else 'Anonymous'

    # Log a warning message including the username and the path causing the 404 error
    logger.warning("User %s encountered a 404 error while accessing: %s", username, request.path)
    
    # Render the 404 error page
    return render(request, "wongnung/404.html", status=404)

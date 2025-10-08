from django.shortcuts import render
import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__) #logging_test.views

def index(request):
    logger.info("Testing the Logger!!")

    try:
        User.objects.get(pk=1)
    except User.DoesNotExist:
        logger.error("User with ID %s does not exist", 1)

    return render(request, "index.html")
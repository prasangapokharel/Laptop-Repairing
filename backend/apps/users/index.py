"""
User module entry point
"""
from .models import User
from .serializers import UserSerializer

__all__ = ['User', 'UserSerializer']

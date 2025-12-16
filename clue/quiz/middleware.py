# quiz/middleware.py
import json
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

class AIGenerationMiddleware(MiddlewareMixin):
    """Track AI question generation for analytics"""
    
    def process_response(self, request, response):
        if request.path == '/quiz/ai/generate/' and request.method == 'POST':
            try:
                if response.status_code == 200:
                    data = json.loads(response.content)
                    if data.get('success'):
                        # Log successful generation
                        from django.contrib.auth.models import AnonymousUser
                        if not isinstance(request.user, AnonymousUser):
                            from .models import AIGenerationLog
                            AIGenerationLog.objects.create(
                                user=request.user,
                                model=data.get('model_used', 'unknown'),
                                topic=request.POST.get('topic', ''),
                                question_count=data.get('count', 0),
                                success=True
                            )
            except:
                pass
        
        return response

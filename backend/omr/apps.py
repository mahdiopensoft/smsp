import os
import sys
import threading
from django.apps import AppConfig

class OmrConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'omr'

    def ready(self):
        # Warm up AI verifier models on GPU in background to eliminate Cold Start latency
        is_server = any(cmd in sys.argv[0] or cmd in sys.argv for cmd in ['runserver', 'daphne', 'gunicorn', 'uvicorn']) or os.environ.get('RUN_MAIN') == 'true'
        if is_server:
            def _warmup():
                try:
                    import time
                    time.sleep(1.5)
                    from omr.providers.ai_verification import get_ai_verifier
                    verifier = get_ai_verifier()
                    import numpy as np
                    dummy = [np.ones((64, 64, 3), dtype=np.uint8)]
                    verifier.predict_batch(dummy)
                except Exception:
                    pass
            threading.Thread(target=_warmup, daemon=True).start()

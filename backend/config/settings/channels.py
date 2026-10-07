"""
إعدادات Channels و ASGI
"""
from decouple import config

# ═══════════════════════════════════════════════════════════════════════════════
# 🔌 ASGI Application
# ═══════════════════════════════════════════════════════════════════════════════
ASGI_APPLICATION = 'config.asgi.application'

# ═══════════════════════════════════════════════════════════════════════════════
# 📡 Channel Layers
# ═══════════════════════════════════════════════════════════════════════════════
CHANNEL_LAYER_TYPE = config('CHANNEL_LAYER_TYPE', default='memory')

if CHANNEL_LAYER_TYPE == 'redis':
    # استخدام Redis للإنتاج
    REDIS_HOST = config('REDIS_HOST', default='localhost')
    REDIS_PORT = config('REDIS_PORT', default='6379')
    
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [(REDIS_HOST, int(REDIS_PORT))],
                'capacity': config('CHANNEL_CAPACITY', default=1500, cast=int),
                'expiry': config('CHANNEL_EXPIRY', default=10, cast=int),
            },
        },
    }
else:
    # استخدام الذاكرة للتطوير
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }

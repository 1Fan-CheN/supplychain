class Config:
    DEBUG = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False


Config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

        

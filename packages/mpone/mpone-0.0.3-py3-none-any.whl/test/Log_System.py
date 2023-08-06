from loguru import logger

trace = logger.add('runtime.log')
logger.debug('this is a debug message')
logger.remove(trace)
logger.debug('this is another debug message')

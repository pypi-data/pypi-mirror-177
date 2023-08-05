import os
import sys
import logging
import logging.handlers as handlers

def getLogger(logger_name, log_folder_full_path=None, log_level=None, save_debug_log=False):
    logger = logging.getLogger(logger_name)

    if len(logger.handlers) < 4:
        # the logger is a new one
        if log_folder_full_path is None:
            log_folder_full_path = os.environ.get("MyLogger_LogFolder","")

        if log_level is None:
            log_level = os.environ.get("MyLogger_LogLevel","WARNING")
        logger.setLevel(log_level)

        # Set Error and Fatal
        error_log_format="%(asctime)s - %(message)s"
        error_log_handler = handlers.TimedRotatingFileHandler(os.path.join(log_folder_full_path,logger_name+"_error.log"), when="D", interval=1, backupCount=30)
        error_log_handler.setLevel(logging.ERROR)
        error_log_handler.setFormatter(logging.Formatter(error_log_format))
        # Set Warning
        warn_log_format="%(asctime)s - %(message)s"
        warn_log_handler = handlers.RotatingFileHandler(os.path.join(log_folder_full_path,logger_name+"_warn.log"), maxBytes=500000000, backupCount=10)
        warn_log_handler.setLevel(logging.WARNING)
        warn_log_handler.setFormatter(logging.Formatter(warn_log_format))
        # Set Info
        info_log_format="%(asctime)s - %(message)s"
        info_log_handler = handlers.RotatingFileHandler(os.path.join(log_folder_full_path,logger_name+"_info.log"), maxBytes=1000000000, backupCount=3)
        info_log_handler.setLevel(logging.INFO)
        info_log_handler.setFormatter(logging.Formatter(info_log_format))
        # Set Debug
        debug_log_format="%(asctime)s - %(message)s"
        if save_debug_log:
            debug_log_handler = handlers.RotatingFileHandler(os.path.join(log_folder_full_path,logger_name+"_debug.log"), maxBytes=1000000000, backupCount=3)
        else:
            debug_log_handler = logging.StreamHandler(sys.stdout)
        debug_log_handler.setLevel(logging.DEBUG)
        debug_log_handler.setFormatter(logging.Formatter(debug_log_format))
        
        
        logger.addHandler(error_log_handler)
        logger.addHandler(warn_log_handler)
        logger.addHandler(info_log_handler)
        logger.addHandler(debug_log_handler)

    return logger
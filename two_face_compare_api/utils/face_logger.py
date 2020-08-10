import logging
import logging.handlers

def log_fun():
    logger = logging.getLogger('ocr')
    logger.setLevel(logging.DEBUG)

    # formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(lineno)06d | %(message)s')

    file_handler = logging.handlers.TimedRotatingFileHandler('/var/www/ekyc_two_face_compare/two_face_compare_api/logs/face_match_base_file', 'D')
    # file_handler.suffix = "log"
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
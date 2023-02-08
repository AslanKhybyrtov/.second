import logging
logging.basicConfig(level=logging.INFO,
    filename="logs.log",
    format="%(asctime)s - %(module)s\n[%(levelname)s] %(funcName)s:\n %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
    encoding="utf-8")


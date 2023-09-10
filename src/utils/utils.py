import logging

from src.shared.exceptions import GenericException


def error_wrapper(logger: logging.Logger, def_error_msg: str = None):
    def outer_wrapper(func):
        def inner_wrapper(*args):
            try:
                return func(args)
            except GenericException as e:
                logger.exception(e)
                raise
            except Exception as e:
                logger.exception(e)

                if def_error_msg is None:
                    raise Exception(f'Unhandled error occurred in funcition {func}')
                else:
                    raise Exception(def_error_msg)

        return inner_wrapper
    return outer_wrapper

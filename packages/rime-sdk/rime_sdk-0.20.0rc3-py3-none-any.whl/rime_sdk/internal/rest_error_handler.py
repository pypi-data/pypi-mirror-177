"""Context manager to handle REST errors."""
import ast
from types import TracebackType
from typing import Optional, Type

from rime_sdk.swagger.swagger_client.rest import ApiException


class RESTErrorHandler:
    """Class that can be used as a context manager.

    Used so that we handle REST errors in a uniform way in the code base.
    """

    def __enter__(self) -> None:
        """Needed for context manager usage."""

    def __exit__(  # pylint: disable=useless-return
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        """Handle exceptions in custom way on exit."""
        # Check if an exception was raised.
        if exc_type is not None:
            # For ApiException errors, we only raise the details.
            if isinstance(exc, ApiException):
                if exc.body:
                    body_string = exc.body.decode("UTF-8")
                    body_dict = ast.literal_eval(body_string)
                    raise ValueError(f"{exc.reason}: {body_dict['message']}") from None
                else:
                    raise ValueError(exc.reason)
        # Returning None will raise any other error messages as they were.
        return None

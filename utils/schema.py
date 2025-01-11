from collections.abc import Callable
from typing import Any, get_args, get_origin


def function_to_openai_schema(func: Callable[..., Any]) -> dict:
    """
    Converts a Python function into an OpenAI-compatible tool schema.
    """
    import inspect

    # Mapping Python types to JSON schema types
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    def resolve_type(annotation):
        """
        Resolves a Python type annotation to a JSON schema-compatible type.
        """
        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin is None:  # Simple type
            return type_map.get(annotation, "string")

        if origin is list:  # List type
            item_type = resolve_type(args[0]) if args else "string"
            return {"type": "array", "items": {"type": item_type}}

        if origin is dict:  # Dict type
            return {"type": "object"}  # Simplified, no detailed structure

        return "string"  # Fallback for unsupported types

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    properties = {}
    required = []

    for param in signature.parameters.values():
        param_annotation = (
            param.annotation if param.annotation != inspect.Parameter.empty else Any
        )
        param_type = resolve_type(param_annotation)

        properties[param.name] = {
            "type": param_type if isinstance(param_type, str) else param_type["type"],
            "description": f"The {param.name} parameter.",
        }

        if param.default == inspect.Parameter.empty:  # No default value means required
            required.append(param.name)

    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "No description provided.",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required if required else [],
            },
        },
    }

"""
    Book schemas
"""

add_book_schema = {
    "type": "object",
    "properties": {
        "isbn": {"type": "string"}
    },
    "required": ["isbn"]
}

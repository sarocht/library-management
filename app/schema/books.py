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

update_book_schema = {
    "type": "object",
    "properties": {
        "isbn": {"type": "string"},
        "title": {"type": "string"},
        "subtitle": {"type": "string"},
        "publisher": {"type": "string"},
        "published_date": {"type": "string"},
        "page_count": {"type": "integer"},
        "info_link": {"type": "string"},
        "status": {"type": "string"},
        "created_date": {"type": "string"},
    },
    "required": ["isbn"]
}

delete_book_schema = {
    "type": "object",
    "properties": {
        "isbn": {"type": "string"},
    },
    "required": ["isbn"]
}

borrow_book_schema = {
    "type": "object",
    "properties": {
        "isbn": {"type": "string"},
        "created_by": {"type": "string"},
        "borrowed_by": {"type": "string"},
    },
    "required": ["isbn", "created_by", "borrowed_by"]
}
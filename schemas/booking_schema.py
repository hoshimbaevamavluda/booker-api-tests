BOOKING_SCHEMA = {
    "type": "object",
    "required": ["firstname", "lastname", "totalprice", "depositpaid", "bookingdates"],
    "properties": {
        "firstname": {"type": "string", "minLength": 1},
        "lastname": {"type": "string"},
        "totalprice": {"type": "integer", "minimum": 0},
        "depositpaid": {"type": "boolean"},
        "bookingdates": {
            "type": "object",
            "required": ["checkin", "checkout"],
            "properties": {
                "checkin": {"type": "string", "format": "date"},
                "checkout": {"type": "string", "format": "date"}
            }
        },
        "additionalneeds": {"type": ["string", "null"]}
    },
    "additionalProperties": False
}
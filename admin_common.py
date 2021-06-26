def foreign_field(field_name):
    def accessor(obj):
        val = obj
        for part in field_name.split("__"):
            val = getattr(val, part) if val else None
        return val

    accessor.__name__ = str(field_name)
    return accessor


def many_to_many_field(field_name):
    def accessor(obj):
        related_field, field_to_display = field_name.split("__")
        display_res = [
            getattr(each_object, field_to_display)
            for each_object in getattr(obj, related_field).all()
        ]
        return ", ".join(sorted(display_res))

    accessor.__name__ = field_name
    return accessor


ff = foreign_field
mf = many_to_many_field

import json


class Str(str):
    pass


class Float(float):
    pass


class Int(int):
    pass


class Dict(dict):
    pass


class List(list):
    pass


def make_response(items):
    res = []
    for item in items:
        item_data = item["data"]

        try:
            item_data = json.loads(item_data)
        except:
            ...

        try:
            if "." in item_data:
                item_data = float(item_data)
            item_data = int(item_data)
        except:
            ...

        formatted = None
        if type(item_data) == str:
            formatted = Str(item_data)
            try:
                formatted.size = item["size"]
                formatted.total_size = item["total_size"]

                formatted.content_type = item["content_type"]
                formatted.created = item["created"]
                formatted.updated = item["updated"]
            except:
                pass

        elif type(item_data) == float:
            formatted = Float(item_data)
            try:
                formatted.size = item["size"]
                formatted.total_size = item["total_size"]

                formatted.content_type = item["content_type"]
                formatted.created = item["created"]
                formatted.updated = item["updated"]
            except:
                pass

        elif type(item_data) == int:
            formatted = Int(item_data)
            try:
                formatted.size = item["size"]
                formatted.total_size = item["total_size"]

                formatted.content_type = item["content_type"]
                formatted.created = item["created"]
                formatted.updated = item["updated"]
            except:
                pass

        elif type(item_data) == dict:
            formatted = Dict(item_data)
            try:
                formatted.size = item["size"]
                formatted.total_size = item["total_size"]

                formatted.content_type = item["content_type"]
                formatted.created = item["created"]
                formatted.updated = item["updated"]
            except:
                pass

        elif type(item_data) == list:
            formatted = List(item_data)
            try:
                formatted.size = item["size"]
                formatted.total_size = item["total_size"]

                formatted.content_type = item["content_type"]
                formatted.created = item["created"]
                formatted.updated = item["updated"]
            except:
                pass
        if formatted:
            res.append(formatted)

    return res

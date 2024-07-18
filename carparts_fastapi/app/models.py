class Mark:
    def __init__(self, id, name, producer_country_name, is_visible):
        self.id = id
        self.name = name
        self.producer_country_name = producer_country_name
        self.is_visible = is_visible


class Model:
    def __init__(self, id, name, mark_id, is_visible):
        self.id = id
        self.name = name
        self.mark_id = mark_id
        self.is_visible = is_visible


class Part:
    def __init__(self, id, name, mark_id, model_id, price, json_data, is_visible):
        self.id = id
        self.name = name
        self.mark_id = mark_id
        self.model_id = model_id
        self.price = price
        self.json_data = json_data
        self.is_visible = is_visible

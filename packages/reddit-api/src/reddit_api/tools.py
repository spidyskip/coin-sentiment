from datetime import datetime


class GeneratorID:
    @staticmethod
    def id_number_generator():
        now = datetime.now()
        return int(now.timestamp())

    @staticmethod
    def get_date(generated_id):
        return datetime.fromtimestamp(generated_id)

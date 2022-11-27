class Utils:
    @staticmethod
    def model_to_dict(model):
        return {c.name: getattr(model, c.name) for c in model.__table__.columns}

    @staticmethod
    def lmodel_to_ldict(models):
        array = []
        for model in models:
            array.append(Utils.model_to_dict(model))
        return array

    @staticmethod
    def lrow_to_ldict(rows):
        ldict = []
        ldict = [record._mapping for record in rows]
        return ldict

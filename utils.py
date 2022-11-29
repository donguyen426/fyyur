import babel
import dateutil.parser


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

    def convert_genres(strGenres):
        listGenres = []
        listGenres = (
            strGenres.replace("{", "").replace("}", "").replace('"', "").split(",")
        )
        return listGenres

    def format_datetime(value, format="medium"):
        date = dateutil.parser.parse(value)
        if format == "full":
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == "medium":
            format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format, locale="en")

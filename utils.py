import babel
import dateutil.parser


class Utils:
    def model_to_dict(model):
        """Convert a db.Model to a dict"""
        return {c.name: getattr(model, c.name) for c in model.__table__.columns}

    def lmodel_to_ldict(models):
        """Convert a list of db.Model to a list of dict"""
        array = []
        for model in models:
            array.append(Utils.model_to_dict(model))
        return array

    def lrow_to_ldict(rows):
        """Convert a list of SQLAlchemy rows to a list of dict"""
        ldict = []
        ldict = [record._mapping for record in rows]
        return ldict

    def format_datetime(value, format="medium"):
        date = dateutil.parser.parse(value)
        if format == "full":
            format = "EEEE MMMM, d, y 'at' h:mma"
        elif format == "medium":
            format = "EE MM, dd, y h:mma"
        return babel.dates.format_datetime(date, format, locale="en")

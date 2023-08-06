from shopcloud_django_toolbox import id_generator
from . import models


def generate_source(**kwargs) -> models.Source:
    obj, created = models.Source.objects.get_or_create(
        code=id_generator(),
        type=kwargs.get('type', models.SourceType.SAGE_SQL_CONNECTOR_V1),
    )
    return obj


def generate_metric(**kwargs) -> models.Metric:
    source = generate_source()
    obj, created = models.Metric.objects.get_or_create(
        code=id_generator(),
        source=source,
    )
    return obj

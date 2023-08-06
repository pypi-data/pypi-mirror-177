from typing import Tuple, Optional

from django.conf import settings
from shopcloud_django_instrumenting import tracing
import requests

from monitoring import models


class Plugin:
    NAME = "SAGE_SQL_CONNECTOR_V1"

    def proceed(self, span: tracing.Span, metric: models.Metric, **kwargs) -> Tuple[bool, Optional[int]]:
        if settings.TEST_MODE:
            return True, 5

        with span.start_span('product-description-generate') as sub_span:
            url = f'https://{metric.source.meta_api_endpoint}/databases/sage/query'
            sub_span.set_tag('url', url)
            sub_span.set_tag('method', 'POST')
            response = requests.post(
                url,
                headers={
                    'X-API-KEY': metric.source.meta_api_password,
                    'UserAgent': 'markeptlace-suppliers',
                },
                json={
                    'query': metric.query,
                }
            )
            sub_span.set_tag('status_code', str(response.status_code))
            if not (200 <= response.status_code <= 299):
                if response.status_code == 404:
                    return False, 0
                sub_span.log_kv(response.json())
                return False, 0
            data = response.json()
            return True, data.get('total', 0)

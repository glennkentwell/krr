from robusta_krr.core.models.allocations import ResourceType
from robusta_krr.core.models.objects import K8sObjectData

from .base_filtered_metric import BaseFilteredMetricLoader
from .base_metric import bind_metric, QueryType


@bind_metric(ResourceType.Memory)
class MemoryMetricLoader(BaseFilteredMetricLoader):
    def get_query(self, object: K8sObjectData) -> str:
        pods_selector = "|".join(pod.name for pod in object.pods)
        cluster_label = self.get_prometheus_cluster_label()
        return (
            f'max(max_over_time(container_memory_max_usage_bytes{{'
            f'namespace="{object.namespace}", '
            f'pod=~"{pods_selector}", '
            f'container="{object.container}"'
            f'{cluster_label}'
            f'}}[14d])) '
            f'by (container, pod, job)'
        )
    
    def get_query_type(self) -> QueryType:
        return QueryType.Query
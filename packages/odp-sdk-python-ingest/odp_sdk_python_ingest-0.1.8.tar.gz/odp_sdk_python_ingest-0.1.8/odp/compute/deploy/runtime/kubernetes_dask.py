import os
import warnings
from typing import Dict, Optional, Union

from dask_kubernetes.operator import KubeCluster
from prefect.flows import Flow
from prefect_dask import DaskTaskRunner

from .kubernetes_tiered_resource import KubernetesTieredResource


class _DaskTaskRunnerWrapper(DaskTaskRunner):
    @property
    def name(self):
        return "ephemeralDask"

    # async def _start(self, *args, **kwargs):
    #     try:
    #         super()._start(*args, **kwargs)
    #     except ValueError as exc:
    #         raise ValueError(f"Cluster = {self._connect_to}") from exc

    def __setstate__(self, state: dict):
        try:
            super().__setstate__(state)
        except ValueError:
            # Ignore value error raised by `distributed.get_client()`
            pass


class KubernetesDask(KubernetesTieredResource):

    ENV_DASK_GATEWAY_ADDRESS = "DASK_GATEWAY_ADDRESS"
    ENV_K8S_SERVICE_ACCOUNT = "K8S_SERVICE_ACCOUNT"

    def __init__(
        self,
        flow: Flow,
        tier: Optional[str] = None,
        cluster_tier: Optional[str] = None,
        min_workers: int = 1,
        max_workers: int = 2,
        namespace: Optional[str] = None,
        env: Optional[Dict[str, Union[None, str]]] = None,
        service_account: Optional[str] = None,
    ):
        warnings.warn("The KubernetesDask runtime is currently not supported")
        super().__init__(flow, tier, namespace, env)

        self._service_account = service_account or os.environ.get(self.ENV_K8S_SERVICE_ACCOUNT, "dask-gateway")

        # Cluster nodes defaults to the same tier as the flow
        self._cluster_tier = cluster_tier or self._tier
        self._min_workers = min_workers
        self._max_workers = max_workers

    def apply_flow_options(self, flow: Flow):

        resources = self.TIERS[self._cluster_tier]

        # extra_labels = {"prefect.io/flow": self._flow.name, "hubocean.io/clusterTier": self._cluster_tier}
        # extra_annotations = {"prefect.io/flow": self._flow.name, "hubocean.io/clusterTier": self._cluster_tier}

        flow.task_runner = _DaskTaskRunnerWrapper(
            cluster_class=KubeCluster,
            cluster_kwargs={
                "name": f"{flow.name}",
                "namespace": self._namespace,
                "image": self._storage.get_name(),
                "n_workers": 1,
                "resources": {
                    # "requests": {
                    #     "cpu": 0.9 * resources.cpu,
                    #     "memory": 0.88 * resources.mem,
                    # },
                    "limits": {
                        "cpu": resources.cpu,
                        "memory": resources.mem,
                    }
                },
            },
            adapt_kwargs={
                "minimum": self._min_workers,
                "maximum": self._max_workers,
            },
            client_kwargs={"set_as_default": True},
        )

    # def get_customizations(self) -> List[Dict[str, Any]]:
    #     customizations = super().get_customizations()

    #     return customizations + [
    #         {
    #             "op": "add",
    #             "path": "/spec/template/spec/serviceAccountName",
    #             "value": self._service_account,
    #         }
    #     ]

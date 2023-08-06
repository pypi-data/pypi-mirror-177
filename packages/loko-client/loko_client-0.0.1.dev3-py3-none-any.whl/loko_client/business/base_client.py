from abc import ABC

from loko_client.business.async_predictor_client import AsyncPredictorsClient, AsyncModelsClient, \
    AsyncTransformersClient, AsyncJobsClient, AsyncContainersClient, AsyncDatasetsClient
from loko_client.business.predictor_client import PredictorsClient, ModelsClient, TransformersClient, JobsClient, \
    ContainersClient, DatasetsClient
from loko_client.utils.requests_utils import URLRequest, AsyncURLRequest


GATEWAY = 'http://localhost:9999/routes/'

class PredictorClient:
    """
        Predictor client.

        Args:
            gateway (str): Gateway URL.
    """
    def __init__(self, gateway=GATEWAY):
        self.u = URLRequest(gateway).predictor
        self.predictors = PredictorsClient(u=self.u)
        self.models = ModelsClient(u=self.u)
        self.transformers = TransformersClient(u=self.u)
        self.jobs = JobsClient(u=self.u)
        self.containers = ContainersClient(u=self.u)
        self.datasets = DatasetsClient(u=self.u)

class AsyncPredictorClient:
    """
        Asynchronous Predictor client.

        Args:
            gateway (str): Gateway URL.
            timeout (float): The maximal number of seconds for the whole operation including connection establishment,
                request sending and response reading. Default: 300
    """
    def __init__(self, gateway=GATEWAY, timeout=None):
        self.u = AsyncURLRequest(gateway, timeout).predictor
        self.predictors = AsyncPredictorsClient(u=self.u)
        self.models = AsyncModelsClient(u=self.u)
        self.transformers = AsyncTransformersClient(u=self.u)
        self.jobs = AsyncJobsClient(u=self.u)
        self.containers = AsyncContainersClient(u=self.u)
        self.datasets = AsyncDatasetsClient(u=self.u)



class OrchestratorClient(ABC):
    """
        An abstract base orchestrator client.
    """

    def __init__(self, gateway=GATEWAY):
        self.u = URLRequest(gateway).orchestrator

class AsyncOrchestratorClient(ABC):
    """
        An abstract base orchestrator client.
    """

    def __init__(self, gateway, timeout=None):
        self.u = AsyncURLRequest(gateway, timeout).orchestrator

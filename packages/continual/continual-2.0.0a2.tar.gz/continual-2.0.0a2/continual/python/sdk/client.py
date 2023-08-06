from __future__ import annotations
import grpc
from typing import Optional
from google.protobuf.empty_pb2 import Empty
from continual.python.sdk.config import Config
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import management_pb2_grpc
from continual.rpc.management.v1 import types
from continual.python.sdk.projects import ProjectManager
from continual.python.sdk.environments import EnvironmentManager
from continual.python.sdk.organizations import OrganizationManager
from continual.python.sdk.featuresets import FeatureSetManager
from continual.python.sdk.runs import RunManager
from continual.python.sdk.models import ModelManager
from continual.python.sdk.users import UserManager, User
from continual.python.sdk.model_versions import ModelVersionManager
from continual.python.sdk.experiments import ExperimentManager
from continual.python.sdk.promotions import PromotionManager
from continual.python.sdk.interceptors import AuthInterceptor
from continual.python.sdk.exceptions import normalize_exceptions_for_class
from continual.python.sdk.batchpredictions import BatchPredictionManager
from continual.python.sdk.events import EventManager
from continual.python.sdk.logger import Logger
from continual.python.utils.client_utils import get_management_channel
from continual.rpc.logging.v1 import logging_pb2_grpc


class Client:
    """Continual client."""

    users: UserManager
    """User manager."""

    projects: ProjectManager
    """Project manager."""

    environments: EnvironmentManager
    """Environment manager."""

    organizations: OrganizationManager
    """Organization manager."""

    feature_sets: FeatureSetManager
    """Feature set manager."""

    models: ModelManager
    """Model manager."""

    runs: RunManager
    """Runs manager"""

    model_versions: ModelVersionManager
    """Model versions manager."""

    experiments: ExperimentManager
    """Experiments manager."""

    promotions: PromotionManager
    """Promotion manager."""

    events: EventManager
    """Events manager."""

    batch_predictions: BatchPredictionManager
    """Batch Prediction  manager"""

    config: Config
    """Client configuration."""

    _management: management_pb2_grpc.ManagementAPIStub
    """Management GRPC API."""

    _logger: logging_pb2_grpc.LoggingAPIStub
    """Logging GRPC API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
        project: Optional[str] = None,
        environment: Optional[str] = None,
    ):
        """Initialize client.

        It is recommended to use `continual login` to generate a
        local on-disk API key.

        Arguments:
            api_key: API key.
            project: Default project.
            endpoint: Cluster endpoint (Private Cloud only)
        """
        self.config = Config(
            api_key=api_key, project=project, environment=environment, endpoint=endpoint
        )

        # Initialize GRPC connections.
        auth_interceptor = AuthInterceptor(lambda: self.config.api_key)

        self._mgmt_channel = get_management_channel(self.config.endpoint)

        self._mgmt_channel = grpc.intercept_channel(
            self._mgmt_channel, auth_interceptor
        )
        self._management = normalize_exceptions_for_class(
            management_pb2_grpc.ManagementAPIStub(self._mgmt_channel)
        )
        self._logger = normalize_exceptions_for_class(
            logging_pb2_grpc.LoggingAPIStub(self._mgmt_channel)
        )

        # Initialize managers.
        parent = self.config.project
        if parent is None:
            parent = "projects/-"
        else:
            env = self.config.environment
            if (
                env == None
                or env == "master"
                or env == "main"
                or env == "production"
                or len(env) == 0
            ):
                env = "prod"
            if env != "prod":
                parent = f"{self.config.project}@{self.config.environment}"

        self.users = UserManager(client=self)
        self.projects = ProjectManager(client=self)
        self.environments = EnvironmentManager(client=self, parent=parent)
        self.runs = RunManager(client=self, parent=parent)
        self.organizations = OrganizationManager(client=self)
        self.feature_sets = FeatureSetManager(client=self, parent=parent)
        self.models = ModelManager(client=self, parent=parent)
        self.model_versions = ModelVersionManager(
            client=self, parent=parent + "/models/-"
        )
        self.experiments = ExperimentManager(
            client=self, parent=parent + "/models/-/versions/-"
        )
        self.promotions = PromotionManager(client=self, parent=parent + "/models/-")
        self.batch_predictions = BatchPredictionManager(
            client=self, parent=parent + "/models/-"
        )
        self.events = EventManager(client=self, parent=parent)

        self.logger = Logger()

    def init(
        self,
        run_id: Optional[str] = None,
        description: Optional[str] = None,
        heartbeat_interval: Optional[int] = 5,
    ):
        """
        Initializes a continual run

        Arguments
        ---------
        run_id: str
            an optional id for a run
        description: str
            A human readable string representing what the current run
            is doing.
        heartbeat_interval: int
            interval in seconds between two heartbeats that the run sends
            to Continual endpoint

        Returns
        -------
        Run
            The run object on which
        """

        run = self.runs.create(
            run_id=run_id,
            description=description,
            heartbeat_interval=heartbeat_interval,
        )
        return run

    def __del__(self) -> None:
        """Clean up active gRPC channels and threads when client deleted."""
        if hasattr(self, "_mgmt_channel"):
            self._mgmt_channel.close()
        if hasattr(self, "_fs_channel"):
            self._fs_channel.close()
        if hasattr(self, "_gw_channel"):
            self._gw_channel.close()
        if self.logger and self.logger.hb_thread:
            self.logger.hb_thread.stop()

    def viewer(self) -> User:
        """Currently authenticated user."""
        resp = self._management.GetViewer(Empty())
        return User.from_proto(resp, client=self)

    def register(
        self, first_name: str, last_name: str, email: str, password: str
    ) -> User:
        """Register a new account.

        This function registers and authenticates a new user.  This is
        meant only for automation purposes.  Please sign up directly on
        https://continual.ai instead.

        Arguments:
            first_name: First name of user.
            last_name: Last name of user
            email: Email address.
            password: Password.

        Returns:
            The newly created authenticated user.
        """
        self.config.api_key = ""
        req = management_pb2.RegisterRequest(
            first_name=first_name, last_name=last_name, email=email, password=password
        )
        resp = self._management.Register(req)
        self.config.api_key = resp.auth_token
        self.config.email = email
        return User.from_proto(resp.user, client=self)

    def login(self, email: str, password: str) -> User:
        """Login to Continual.

        It is strongly recommended to use `continual login` CLI
        or an API key instead of logging in via the SDK.

        Args:
            email: Email address.
            password: Password.
        Returns:
            The authenticated user.
        """
        self.config.api_key = ""
        req = management_pb2.LoginRequest(email=email, password=password)
        resp = self._management.Login(req)
        self.config.api_key = resp.auth_token
        self.config.email = email
        return User.from_proto(resp.user, client=self)

    def logout(self) -> None:
        """Logout.

        Logs out current session deleting the associated API key.
        """
        if self.config.api_key is not None and self.config.api_key != "":
            self._management.Logout(Empty())
            self.config.api_key = None
            self.config.email = None
            self.config.save()

    def infer_schema(
        self,
        project: str = None,
        table: str = None,
        query: str = None,
        file: str = None,
        type: str = "FeatureSet",
    ):
        """Infer Schema.

        Infers schema from file or data warehouse table.
        """
        if project is None:
            project = self.config.project
        elif not ("/" in project):
            project = "projects/%s" % project

        if query is not None:
            req = management_pb2.GetInferredSchemaRequest(project=project, query=query)
        elif table is not None:
            query = "SELECT * FROM %s" % table
            req = management_pb2.GetInferredSchemaRequest(project=project, query=query)
        elif file is not None:
            p = self.projects.get(project)
            (_, table) = p.seed(file)
            query = "SELECT * FROM %s" % table
            req = management_pb2.GetInferredSchemaRequest(project=project, query=query)
        else:
            return {"Error: Either 'table', 'query', or 'file' must be specified"}

        resp = self._management.GetInferredSchema(req)

        schema = []
        for c in resp.columns:
            types.ColumnConfig.from_proto(c)
            schema.append(c)

        return schema

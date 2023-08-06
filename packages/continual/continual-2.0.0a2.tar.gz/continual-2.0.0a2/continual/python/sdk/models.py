from __future__ import annotations
from typing import List, Optional
from continual.rpc.management.v1 import management_pb2
from continual.rpc.management.v1 import types
from continual.python.sdk.resource import Resource
from continual.python.sdk.manager import Manager
from continual.python.sdk.iterators import Pager
from continual.python.sdk.model_versions import ModelVersionManager
from continual.python.sdk.promotions import PromotionManager
from continual.python.sdk.events import EventManager
from continual.python.sdk.tags import TagsManager
from continual.python.sdk.metadata import MetadataManager


from continual.python.sdk.batchpredictions import (
    BatchPredictionManager,
)


class ModelManager(Manager):
    """Manages model resources."""

    name_pattern: str = "projects/{project}/models/{model}"

    def create(
        self,
        display_name: str,
        description: Optional[str] = "",
        if_not_exists: bool = True,
    ) -> Model:
        """Create model.

        Arguments:
            id: Model name or id.

        Returns
            An experiment.
        """
        req = management_pb2.CreateModelRequest(
            name=self.name(display_name),
            description=description,
            if_not_exists=if_not_exists,
        )
        resp = self.client._management.CreateModel(req)
        return Model.from_proto(resp, client=self.client, parent_run=self.run_name)

    def get(self, id: str) -> Model:
        """Get model.

        Arguments:
            id: Model name or id.

        Returns
            An experiment.
        """
        req = management_pb2.GetModelRequest(name=self.name(id))
        resp = self.client._management.GetModel(req)
        return Model.from_proto(resp, client=self.client, parent_run=self.run_name)

    def list(
        self,
        page_size: Optional[int] = None,
        filters: List[str] = None,
        all_projects: bool = False,
    ) -> List[Model]:
        """List model.

        Arguments:
            page_size: Number of items to return.

        Returns:
            A list of models.
        """
        req = management_pb2.ListModelsRequest(
            parent=self.parent,
            page_size=page_size,
            filters=filters,
            all_projects=all_projects,
        )
        resp = self.client._management.ListModels(req)
        return [Model.from_proto(x, client=self.client) for x in resp.models]

    def list_all(self) -> Pager[Model]:
        """List all model.

        Pages through all model using an iterator.

        Returns:
            A iterator of all model.
        """

        def next_page(next_page_token):
            req = management_pb2.ListModelsRequest(
                parent=self.parent, page_token=next_page_token
            )
            resp = self.client._management.ListModels(req)
            return (
                [Model.from_proto(x, client=self.client) for x in resp.models],
                resp.next_page_token,
            )

        return Pager(next_page)


class Model(Resource, types.Model):
    """Model resource."""

    name_pattern: str = "projects/{project}/models/{model}"
    manager: ModelManager

    model_versions: ModelVersionManager
    """Model version manager."""

    promotions: PromotionManager
    """Promotion manager."""

    batch_predictions: BatchPredictionManager
    """Batch Prediction  manager."""

    events: EventManager
    """Event manager."""

    tags: TagsManager
    """Tags Manager"""

    metadata: MetadataManager
    """Metadata Manager"""

    def _init(self):
        self.manager = ModelManager(
            parent=self.parent, client=self.client, run_name=self.parent_run
        )
        self.model_versions = ModelVersionManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )
        self.promotions = PromotionManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )
        self.batch_predictions = BatchPredictionManager(
            parent=self.name, client=self.client
        )
        self.events = EventManager(client=self.client, parent=self.name)
        self.tags = TagsManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )
        self.metadata = MetadataManager(
            parent=self.name, client=self.client, run_name=self.parent_run
        )

    def log(self, items: dict):
        """Logs to fields in model"""
        pass

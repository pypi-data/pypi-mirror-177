from uuid import UUID
from dataclasses import dataclass
from propzen.common.service_layer.externalbus import ExternalEvent


@dataclass
class AssetExpenseAdded(ExternalEvent):
    account_id: UUID
    asset_id: UUID

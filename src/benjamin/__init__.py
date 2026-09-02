"""Benjamin constitutional capital-management kernel."""

from .authority import AuthorizationError, authorize
from .book_bridge import BenjaminBookSigner, BookBridgeError, BookProducerIdentity, load_benjamin_book_signer_from_env
from .control_plane import BenjaminControlPlane, ControlPlaneResult, EvidenceLineage
from .domain import (
    AuthorizedExecutionRequest,
    DecisionStatus,
    InvestmentDecision,
    OrderSide,
    Recommendation,
    RiskDecision,
    RiskStatus,
)
from .evidence import EvidenceDraft, EvidencePublisher
from .steward import decide
from .watchman import RiskPolicy, evaluate

__all__ = [
    "AuthorizationError",
    "AuthorizedExecutionRequest",
    "BenjaminBookSigner",
    "BenjaminControlPlane",
    "BookBridgeError",
    "BookProducerIdentity",
    "ControlPlaneResult",
    "DecisionStatus",
    "EvidenceDraft",
    "EvidenceLineage",
    "EvidencePublisher",
    "InvestmentDecision",
    "OrderSide",
    "Recommendation",
    "RiskDecision",
    "RiskPolicy",
    "RiskStatus",
    "authorize",
    "decide",
    "evaluate",
    "load_benjamin_book_signer_from_env",
]

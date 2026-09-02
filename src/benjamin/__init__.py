"""Benjamin constitutional capital-management kernel."""

from .authority import AuthorizationError, authorize
from .book_bridge import BenjaminBookSigner, BookBridgeError, BookProducerIdentity, load_benjamin_book_signer_from_env
from .book_outbox import (
    ACKNOWLEDGED,
    PENDING,
    QUARANTINED,
    BookAcceptance,
    BookOutbox,
    BookOutboxError,
    OutboxConflict,
    PermanentBookDeliveryError,
)
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
from .watchman_book import (
    WatchmanBookAttachment,
    WatchmanBookError,
    WatchmanBookOutbox,
    WatchmanBookSigner,
    build_watchman_governance_payload,
    load_watchman_book_signer_from_env,
    prepare_watchman_book_attachment,
)

__all__ = [
    "ACKNOWLEDGED",
    "AuthorizationError",
    "AuthorizedExecutionRequest",
    "BenjaminBookSigner",
    "BenjaminControlPlane",
    "BookAcceptance",
    "BookBridgeError",
    "BookOutbox",
    "BookOutboxError",
    "BookProducerIdentity",
    "ControlPlaneResult",
    "DecisionStatus",
    "EvidenceDraft",
    "EvidenceLineage",
    "EvidencePublisher",
    "InvestmentDecision",
    "OrderSide",
    "OutboxConflict",
    "PENDING",
    "PermanentBookDeliveryError",
    "QUARANTINED",
    "Recommendation",
    "RiskDecision",
    "RiskPolicy",
    "RiskStatus",
    "WatchmanBookAttachment",
    "WatchmanBookError",
    "WatchmanBookOutbox",
    "WatchmanBookSigner",
    "authorize",
    "build_watchman_governance_payload",
    "decide",
    "evaluate",
    "load_benjamin_book_signer_from_env",
    "load_watchman_book_signer_from_env",
    "prepare_watchman_book_attachment",
]

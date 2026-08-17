from __future__ import annotations

from ares.domain.enums import UserStatus, MembershipRole

def test_enums() -> None:
    assert UserStatus.ACTIVE == "ACTIVE"
    assert UserStatus.INACTIVE == "INACTIVE"
    assert UserStatus.SUSPENDED == "SUSPENDED"

    assert MembershipRole.OWNER == "OWNER"
    assert MembershipRole.ADMIN == "ADMIN"
    assert MembershipRole.RESEARCHER == "RESEARCHER"

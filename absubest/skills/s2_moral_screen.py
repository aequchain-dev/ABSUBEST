"""
S2 — Moral Screen
===================
Mandatory moral screens per P6 (consequentialist) and P6b (deontological).
Also supports P0b existential-risk classification.
"""

from __future__ import annotations

from typing import Any


def run_moral_screens(purpose: str) -> dict[str, str]:
    """Run mandatory moral screens.

    Returns:
        dict with keys:
            "P6": "PASS" | "FAIL"
            "P6b": "PASS" | "FAIL"
            "P0b": "NOT_TRIGGERED" | "TRIGGERED"
    """
    p6_result = screen_consequentialist(purpose)
    p6b_result = screen_deontological(purpose)
    p0b_result = screen_existential_risk(purpose)

    return {
        "P6": p6_result,
        "P6b": p6b_result,
        "P0b": p0b_result,
    }


def screen_consequentialist(purpose: str) -> str:
    """P6 consequentialist screen: would the best-case outcome cause net harm?"""
    net_harm_keywords = [
        "exploit",
        "deceive",
        "manipulate",
        "coerce",
        "harm",
        "suffer",
        "oppress",
        "discriminate",
        "poison",
        "surveillance without consent",
        "weaponize",
        "destruct",
    ]
    pl = purpose.lower()
    found = [kw for kw in net_harm_keywords if kw in pl]
    if found:
        return "FAIL"
    return "PASS"


def screen_deontological(purpose: str) -> str:
    """P6b deontological screen: does purpose violate universalizable duties?"""
    duty_violations = [
        "deceive",
        "coerce",
        "violate autonomy",
        "break promise",
        "breach trust",
        "deny rights",
        "unjust enrichment",
        "deliberately misinform",
        "violate consent",
        "exploit vulnerability",
    ]
    pl = purpose.lower()
    found = [kw for kw in duty_violations if kw in pl]
    if found:
        return "FAIL"
    return "PASS"


def screen_existential_risk(purpose: str) -> str:
    """P0b existential-risk classification."""
    risk_keywords = [
        "superintelligence",
        "human extinction",
        "civilizational collapse",
        "unaligned AGI",
        "existential risk",
        "weaponized AGI",
        "runaway AI",
        "dystopian",
    ]
    pl = purpose.lower()
    found = [kw for kw in risk_keywords if kw in pl]
    if found:
        return "TRIGGERED"
    return "NOT_TRIGGERED"

"""Credentials dataclass (also exported from config.env, kept here for model parity)."""

from dataclasses import dataclass


@dataclass
class Credentials:
    username: str
    password: str

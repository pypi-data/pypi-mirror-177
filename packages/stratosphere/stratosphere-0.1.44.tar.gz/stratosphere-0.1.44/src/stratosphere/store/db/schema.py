from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types.uuid import UUIDType
from stratosphere import config

# Construct a base class for declarative class definitions.
Base = declarative_base()

# Enum defining the status of an experiment.
ExperimentStatus = Enum("ExperimentStatus", ["UNKNOWN", "COMPLETED", "FAILED", "INTERRUPTED"])

# UUID type, to be used in model definitions. By passing binary=False,
# we fall back to the string representation of UUIDs if there's no native type
# (as in SQLite).
uuid_type = UUIDType(binary=False)


class Experiment(Base):
    """Model representing an experiment in the database."""

    __tablename__ = config.db.experiments_table
    id = sa.Column(uuid_type, primary_key=True, default=None)  # noqa
    name = sa.Column(sa.String(250), nullable=False, unique=True)
    environment = sa.Column(sa.String(), nullable=False)
    execution_time = sa.Column(sa.BigInteger(), nullable=False, default=None)
    completion_time = sa.Column(sa.BigInteger(), nullable=False, default=None)
    attributes = sa.Column(sa.String(), nullable=False, default=None)
    serialized = sa.Column(sa.LargeBinary(), nullable=True, default=None)
    # Currently, the status is not used, and it's always set to UNKNOWN.
    # TODO: either use it, or drop it.
    status = sa.Column(
        sa.Enum(ExperimentStatus),
        nullable=False,
        default=ExperimentStatus["UNKNOWN"],
    )

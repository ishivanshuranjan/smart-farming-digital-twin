from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String

from database.connection import Base


class SensorReading(Base):

    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)

    farm_id = Column(
        String,
        nullable=False,
        index=True
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    temperature = Column(
        Float,
        nullable=False
    )

    humidity = Column(
        Float,
        nullable=False
    )

    soil_moisture = Column(
        Float,
        nullable=False
    )

    light = Column(
        Float,
        nullable=False
    )

    rain_probability = Column(
        Float,
        nullable=False
    )

    leaf_wetness = Column(
        Float,
        nullable=False
    )
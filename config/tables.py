from sqlalchemy import Column, DateTime, func, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FactSales(Base):
    """
    FactSales table representing sales transactions in the database.
    
    This table links sales data to users and time dimensions, including the price of each sale.
    It acts as a fact table in a star schema.

    Attributes:
        id (int): The primary key of the sales fact.
        user_id (int): Foreign key referencing the DimUser table (user).
        time_id (int): Foreign key referencing the DimTime table (time).
        price (int): The price of the sale.
    
    Relationships:
        user (DimUser): Relationship to the DimUser table (user who made the sale).
        time (DimTime): Relationship to the DimTime table (time when the sale occurred).
    """
    
    __tablename__ = 'facts_sales'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("dim_user.id"), nullable=False)  # Foreign key pointing to DimUser.id
    time_id = Column(Integer, ForeignKey("dim_time.id"), nullable=False)  # Foreign key pointing to DimTime.id
    price = Column(Integer, nullable=False)
    
    user = relationship("DimUser", back_populates="sales")
    time = relationship("DimTime", back_populates="sales")
    
    def __repr__(self):
        """
        String representation of the FactSales object.

        Returns:
            str: String representation of a sales fact.
        """
        return f"<FactSales(id={self.id}, price={self.price}, user_id={self.user_id}, time_id={self.time_id})>"

    def to_dict(self):
        """
        Converts the FactSales record to a dictionary.

        Returns:
            dict: Dictionary representation of a sales fact record.
        """
        return {
            "id": self.id,
            "price": self.price,
            "user_id": self.user_id,
            "time_id": self.time_id
        }

class DimTime(Base):
    """
    DimTime table representing time-related data in the database.

    This table stores detailed time attributes such as year, semester, trimester, month, and date.
    It acts as a dimension table in a star schema.

    Attributes:
        id (int): The primary key of the time dimension.
        date (datetime): The timestamp of the time record.
        year (int): The year of the time record.
        semester (int): The semester (1 or 2) of the time record.
        trimester (str): The trimester of the time record (e.g., "Q1", "Q2").
        month (str): The month of the time record (e.g., "January", "February").
    
    Relationships:
        sales (FactSales): Relationship to the FactSales table (sales related to this time period).
    """
    
    __tablename__ = 'dim_time'
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, server_default=func.now())
    year = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)
    trimester = Column(String(10), nullable=False)
    month = Column(String(10), nullable=False)
    
    # Relationship to FactSales
    sales = relationship("FactSales", back_populates="time")

    def __repr__(self):
        """
        String representation of the DimTime object.

        Returns:
            str: String representation of a time dimension record.
        """
        return f"<DimTime(id={self.id}, date={self.date})>"
    
    def to_dict(self):
        """
        Converts the DimTime record to a dictionary.

        Returns:
            dict: Dictionary representation of a time record.
        """
        return {
            'id': self.id,
            'date': self.date,
            'year': self.year,
            'semester': self.semester,
            'trimester': self.trimester,
            'month': self.month
        }
        
class DimUser(Base):
    """
    DimUser table representing user-related data in the database.

    This table stores user attributes like the user ID and user key.
    It acts as a dimension table in a star schema.

    Attributes:
        id (int): The primary key of the user dimension.
        user_key (int): A unique key for the user (used for identifying users).

    Relationships:
        sales (FactSales): Relationship to the FactSales table (sales made by the user).
    """
    
    __tablename__ = 'dim_user'
    
    id = Column(Integer, primary_key=True, index=True)
    user_key = Column(Integer, nullable=False)
    
    # Relationship to FactSales
    sales = relationship("FactSales", back_populates="user")
    
    def __repr__(self):
        """
        String representation of the DimUser object.

        Returns:
            str: String representation of a user dimension record.
        """
        return f"<DimUser(id={self.id}, user_key={self.user_key})>"
    
    def to_dict(self):
        """
        Converts the DimUser record to a dictionary.

        Returns:
            dict: Dictionary representation of a user record.
        """
        return {
            'id': self.id,
            'user_key': self.user_key
        }

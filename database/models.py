```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.database_connection import Base

# Association table for the many-to-many relationship between influencers and users
subscription_influencer_table = Table('subscription_influencer', Base.metadata,
    Column('subscription_id', Integer, ForeignKey('subscriptions.id')),
    Column('influencer_id', Integer, ForeignKey('influencers.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(100), nullable=False)
    subscriptions = relationship('Subscription', back_populates='user')

class Influencer(Base):
    __tablename__ = 'influencers'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    products = relationship('Product', back_populates='influencer')
    subscriptions = relationship('Subscription', secondary=subscription_influencer_table, back_populates='influencers')

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    influencer_id = Column(Integer, ForeignKey('influencers.id'), nullable=False)
    messages = Column(Text, nullable=False)
    user = relationship('User', back_populates='conversations')
    influencer = relationship('Influencer', back_populates='conversations')

class Feature(Base):
    __tablename__ = 'features'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    level = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)  # Price in cents
    user = relationship('User', back_populates='subscriptions')
    influencers = relationship('Influencer', secondary=subscription_influencer_table, back_populates='subscriptions')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)  # Price in cents
    influencer_id = Column(Integer, ForeignKey('influencers.id'), nullable=False)
    influencer = relationship('Influencer', back_populates='products')
```
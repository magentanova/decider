from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from Decider.db.db_setup import Base, engine

# class RevokedAuthToken(Base):
#     __tablename__ = 'revoked_auth_tokens'
#     access_token = String(primary_key=True)

#     @staticmethod
#     def check(token):
#         try:
#             RevokedToken.get(token)
#             return True

#         except RevokedToken.DoesNotExist:
#             return False

def serialize_query_result(resultSet):
    return [result.to_dict() for result in resultSet]

Base.serialize_query_result = serialize_query_result

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=1)
    def __repr__(self): 
        return "<Question active={active} id={id} text={text} />".format(active=self.active, id=self.id, text=self.text)
    def to_dict(self):
        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        d = {}
        for col in columns: 
            val = getattr(self, col)
            d[col] = str(val)
        return d

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    active = Column(Boolean, default=1)
    def __repr__(self): 
        return "<Token active={active} id={id} name={name} />".format(active=self.active, id=self.id, name=self.name)
    def to_dict(self):
        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        d = {}
        for col in columns: 
            val = getattr(self, col)
            d[col] = str(val)
        return d

class QuestionEffect(Base): 
    __tablename__ = "question_effects"
    id = Column(Integer, primary_key=True)
    token_id = Column(ForeignKey('tokens.id'), nullable=False)
    question_id = Column(ForeignKey('questions.id'), nullable=False)
    delta = Column(Integer, nullable=False)
    token = relationship(
        "Token",
        uselist=False,
    )
    question = relationship(
        "Question",
        uselist=False,
    )
    def to_dict(self):
        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        d = {}
        for col in columns: 
            val = getattr(self, col)
            d[col] = str(val)
        for relationship in relationships:
            d[relationship] = getattr(self, relationship).to_dict()
        return d


class TokenValue(Base):
    __tablename__ = "token_values"
    id = Column(Integer, primary_key=True)
    token_id = Column(ForeignKey('tokens.id'), nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    value = Column(Integer, default=50)
    token = relationship(
        "Token",
        uselist=False,
    )
    def to_dict(self):
        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        d = {}
        for col in columns: 
            val = getattr(self, col)
            d[col] = str(val)
        for relationship in relationships:
            print(relationship)
            d[relationship] = getattr(self, relationship).to_dict()
        return d

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

if __name__ == "__main__": 
    Base.metadata.create_all(bind=engine)

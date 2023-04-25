from sqlalchemy import create_engine, TIMESTAMP, Boolean, Column, Integer, String, ForeignKey, REAL, BigInteger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship, Session


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(String, primary_key=True, nullable=False)
    archive_path = Column(String, nullable=False)
    number_of_task = Column(Integer, nullable=False)
    result = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_last = Column(Boolean, default=False)
    captains_tasks = relationship('CaptainTask', back_populates='task')


class Team(Base):
    __tablename__ = 'teams'

    team_name = Column(String, primary_key=True, nullable=False)
    captains = relationship('Captain', back_populates='team')


class Captain(Base):
    __tablename__ = 'captains'

    tg_name = Column(String, primary_key=True, nullable=False)
    team_name = Column(String, ForeignKey('teams.team_name'), nullable=False, unique=True)
    points = Column(REAL, default=0)
    is_first_start = Column(Boolean, default=True)
    team = relationship('Team', back_populates='captains')
    tg_id = Column(BigInteger, nullable=True)
    captains_tasks = relationship('CaptainTask', back_populates='captain')


class CaptainTask(Base):
    __tablename__ = 'captains_tasks'

    captain_task_id = Column(Integer, autoincrement=True, primary_key=True)
    tg_name = Column(String, ForeignKey('captains.tg_name'), nullable=False)
    task_id = Column(String, ForeignKey('tasks.task_id'), nullable=False)
    true_response_date = Column(TIMESTAMP, nullable=True)
    captain = relationship('Captain', back_populates='captains_tasks')
    task = relationship('Task', back_populates='captains_tasks')


class DbRepository:
    def __init__(self, connect_string):
        engine = create_engine(connect_string)

        self.db = Session(autoflush=False, bind=engine)

    def find_first(self, table, predicate):
        return self.db.query(table).filter(predicate).first()

    def find_all(self, table, predicate):
        if predicate is None:
            return self.db.query(table).all()

        return self.db.query(table).filter(predicate).all()

    def add(self, new_data):
        self.db.add(new_data)
        self.db.commit()

    def close(self):
        self.db.close()

import uuid
import enum

from sqlalchemy import orm
from datetime import datetime
from sqlalchemy.types import Enum
from viggocore.database import db
from viggocore.common.subsystem import entity


class MessageType(enum.Enum):
    Info = 0
    Warning = 1
    Error = 2


class Status(enum.Enum):
    Pendente = 0
    Sucesso = 1
    Erro = 2


class IBPTSync(entity.Entity, db.Model):

    attributes = ['ibpt_id', 'status', 'sigla_uf', 'id']

    ibpt_id = db.Column(db.CHAR(32), db.ForeignKey("ibpt.id"), nullable=True)
    ibpt = orm.relationship("IBPT", backref=orm.backref('ibpt'))
    messages = orm.relationship(
        "IBPTSyncMessage", backref=orm.backref('ibpt_sync'),
        cascade='delete,delete-orphan,save-update')
    status = db.Column(Enum(Status), nullable=False)
    sigla_uf = db.Column(db.CHAR(2), nullable=False)

    def __init__(self, id, sigla_uf, ibpt_id=None, status=None,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None, tag=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by, tag)
        self.sigla_uf = sigla_uf
        self.status = status if status else Status.Pendente
        self.ibpt_id = ibpt_id

    def addMsg(self, msg_type, msg_body):
        message = IBPTSyncMessage(
            id=uuid.uuid4().hex, ibpt_sync_id=self.id,
            created_at=datetime.now(), type=msg_type, body=msg_body)
        self.messages.append(message)

    def contains_error(self):
        error = False
        for message in self.messages:
            if message.type == MessageType.Error:
                error = True
                break
        return error

    @classmethod
    def individual(cls):
        return 'ibpt_sync'

    @classmethod
    def embedded(cls):
        return ['messages']


class IBPTSyncMessage(entity.Entity, db.Model):

    attributes = ['ibpt_sync_id', 'type', 'body']
    attributes += entity.Entity.attributes

    ibpt_sync_id = db.Column(
        db.CHAR(32), db.ForeignKey("ibpt_sync.id"), nullable=False)
    type = db.Column(Enum(MessageType), nullable=False)
    body = db.Column(db.String(250), nullable=False)

    def __init__(self, id, ibpt_sync_id, type, body,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by)
        self.ibpt_sync_id = ibpt_sync_id
        self.type = type
        self.body = body

    @classmethod
    def individual(cls):
        return 'ibpt_sync_message'

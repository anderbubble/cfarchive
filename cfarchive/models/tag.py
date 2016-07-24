from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    relationship,
)
from .meta import Base


class Tag (Base):
    __tablename__ = 'tags'

    type_ = Column(String, name='type', primary_key=True)
    object_id = Column(String, ForeignKey('objects.id'), primary_key=True)
    value = Column(Text, nullable=True, primary_key=True)
    object_ = relationship('Object')

    def __json__ (self, include_object=True):
        json = {'type': self.type_,
                'value': self.value}
        if include_object:
            json['object'] = self.object_.__json__(include_tags=False)
        return json

    def __str__ (self):
        if self.value is not None:
            return '{0}[{1}]'.format(self.type_, self.value)
        else:
            return self.type_


    def __eq__ (self, other_tag):
        return (
            self.type_ == other_tag.type_
            and self.value == other_tag.value)

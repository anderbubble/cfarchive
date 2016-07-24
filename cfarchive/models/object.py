import hashlib
import ipfsApi
import mimetypes
import os
import sqlalchemy.orm.exc

from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import (
    relationship,
)

from .meta import Base, method_callback_wrapper, MagicBufferProcessor
from .tag import Tag

from chardet.universaldetector import UniversalDetector


class Object (Base):
    __tablename__ = 'objects'
    id_ = Column(String, name='id', primary_key=True)
    tags = relationship('Tag')

    def apply_tag (self, tag_type, value=None):
        new_tag = Tag(type_=tag_type, value=value)
        if not [tag for tag in self.tags if tag == new_tag]:
            self.tags.append(new_tag)

    def __str__ (self):
        for tag in self.tags:
            if tag.type_ == 'filename' and tag.value:
                return tag.value
        else:
            return ''.join(self.id_[:11], '...')

    def __json__ (self, include_tags=True):
        json = {'id': self.id_}
        if include_tags:
            json['tags'] = [tag.__json__(include_object=False) for tag in self.tags]
        return json

    @classmethod
    def from_file (cls, file_, file_name=None, content_type=None, dbsession=None):
        file_name = file_.name if file_name is None else file_name
        content_types = [] if content_type is None else [content_type]
        file_name_prefix, file_name_extension = os.path.splitext(file_name)
        file_name_type, file_name_encoding = mimetypes.guess_type(file_name, strict=False)
        if file_name_type:
            content_types.append(file_name_type)

        magic = MagicBufferProcessor(mime=True)
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        detector = UniversalDetector()
        file_.read = method_callback_wrapper(file_.read, [
            magic.process,
            md5.update,
            sha1.update,
            detector.feed,
        ])

        ipfs = ipfsApi.Client('127.0.0.1', 5001)
        ipfs_response = ipfs.add(file_)

        if magic.type_:
            content_types.append(magic.type)

        object_ = None
        id_ = os.path.join('/ipfs', ipfs_response['Hash'])
        if dbsession is not None:
            try:
                object_ = dbsession.query(cls).filter_by(id_=id_).one()
            except sqlalchemy.orm.exc.NoResultFound:
                pass
        if not object_:
            object_ = cls(id_=id_)
        object_.apply_tag('filename', file_name)
        object_.apply_tag('extension', file_name_extension)
        if file_name_encoding is not None:
            object_.apply_tag('encoding', file_name_encoding)
        if detector.done:
            object_.apply_tag('encoding', detector.result['encoding'])
        for content_type_ in content_types:
            object_.apply_tag('type', content_type)
        object_.apply_tag('md5', md5.hexdigest())
        object_.apply_tag('sha1', sha1.hexdigest())
        return object_

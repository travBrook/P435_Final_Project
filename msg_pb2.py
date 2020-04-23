# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: msg.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='msg.proto',
  package='kvstore',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\tmsg.proto\x12\x07kvstore\"\xda\x02\n\x07Message\x12\n\n\x02ip\x18\x01 \x01(\t\x12(\n\x06\x63onsis\x18\x02 \x01(\x0e\x32\x18.kvstore.Message.ConType\x12)\n\x07request\x18\x03 \x01(\x0e\x32\x18.kvstore.Message.ReqType\x12%\n\x03\x61\x63k\x18\x04 \x01(\x0e\x32\x18.kvstore.Message.AckType\x12\x0c\n\x04\x64\x61ta\x18\x05 \x01(\t\x12\x12\n\nnum_chunks\x18\x06 \x01(\x03\x12\x0f\n\x07L_Clock\x18\x07 \x01(\x05\"P\n\x07\x43onType\x12\x0b\n\x07NO_TYPE\x10\x00\x12\x0e\n\nLINEARIZED\x10\x01\x12\x0e\n\nSEQUENTIAL\x10\x02\x12\n\n\x06\x43\x41USAL\x10\x03\x12\x0c\n\x08\x45VENTUAL\x10\x04\"%\n\x07ReqType\x12\x08\n\x04NULL\x10\x00\x12\x07\n\x03SET\x10\x01\x12\x07\n\x03GET\x10\x02\"\x1b\n\x07\x41\x63kType\x12\x08\n\x04\x46\x41IL\x10\x00\x12\x06\n\x02OK\x10\x01\x62\x06proto3'
)



_MESSAGE_CONTYPE = _descriptor.EnumDescriptor(
  name='ConType',
  full_name='kvstore.Message.ConType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NO_TYPE', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LINEARIZED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SEQUENTIAL', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CAUSAL', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EVENTUAL', index=4, number=4,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=221,
  serialized_end=301,
)
_sym_db.RegisterEnumDescriptor(_MESSAGE_CONTYPE)

_MESSAGE_REQTYPE = _descriptor.EnumDescriptor(
  name='ReqType',
  full_name='kvstore.Message.ReqType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NULL', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SET', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GET', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=303,
  serialized_end=340,
)
_sym_db.RegisterEnumDescriptor(_MESSAGE_REQTYPE)

_MESSAGE_ACKTYPE = _descriptor.EnumDescriptor(
  name='AckType',
  full_name='kvstore.Message.AckType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FAIL', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OK', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=342,
  serialized_end=369,
)
_sym_db.RegisterEnumDescriptor(_MESSAGE_ACKTYPE)


_MESSAGE = _descriptor.Descriptor(
  name='Message',
  full_name='kvstore.Message',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='kvstore.Message.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='consis', full_name='kvstore.Message.consis', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='request', full_name='kvstore.Message.request', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ack', full_name='kvstore.Message.ack', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='data', full_name='kvstore.Message.data', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='num_chunks', full_name='kvstore.Message.num_chunks', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='L_Clock', full_name='kvstore.Message.L_Clock', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MESSAGE_CONTYPE,
    _MESSAGE_REQTYPE,
    _MESSAGE_ACKTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=369,
)

_MESSAGE.fields_by_name['consis'].enum_type = _MESSAGE_CONTYPE
_MESSAGE.fields_by_name['request'].enum_type = _MESSAGE_REQTYPE
_MESSAGE.fields_by_name['ack'].enum_type = _MESSAGE_ACKTYPE
_MESSAGE_CONTYPE.containing_type = _MESSAGE
_MESSAGE_REQTYPE.containing_type = _MESSAGE
_MESSAGE_ACKTYPE.containing_type = _MESSAGE
DESCRIPTOR.message_types_by_name['Message'] = _MESSAGE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'msg_pb2'
  # @@protoc_insertion_point(class_scope:kvstore.Message)
  })
_sym_db.RegisterMessage(Message)


# @@protoc_insertion_point(module_scope)

# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fightTheLandlord_poker.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)


from common import poker_pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='fightTheLandlord_poker.proto',
  package='fightTheLandlord_poker',
  serialized_pb='\n\x1c\x66ightTheLandlord_poker.proto\x12\x16\x66ightTheLandlord_poker\x1a\x0bpoker.proto\"\x0e\n\x0c\x43_S_OpenHand\"X\n\x0f\x43_S_RobLandlord\x12\x34\n\tchoseType\x18\x01 \x02(\x0e\x32!.fightTheLandlord_poker.CALL_TYPE\x12\x0f\n\x07operate\x18\x02 \x02(\x07\"#\n\x0f\x43_S_SetMultiple\x12\x10\n\x08multiple\x18\x01 \x02(\x07\"\x0e\n\x0cS_C_OpenHand\"P\n\x10S_C_OpenHandData\x12<\n\x0eplayerHandData\x18\x01 \x03(\x0b\x32$.fightTheLandlord_poker.OpenHandData\"/\n\x0cOpenHandData\x12\x0c\n\x04side\x18\x01 \x02(\x07\x12\x11\n\thandCards\x18\x02 \x03(\t\"m\n\x0fS_C_RobLandlord\x12\x0c\n\x04side\x18\x01 \x02(\x07\x12\x34\n\tchoseType\x18\x02 \x01(\x0e\x32!.fightTheLandlord_poker.CALL_TYPE\x12\x16\n\x0e\x63\x61nChooseScore\x18\x03 \x03(\x07\"\xc3\x01\n\x15S_C_RobLandlordResult\x12\x0c\n\x04side\x18\x01 \x02(\x07\x12\x34\n\tchoseType\x18\x02 \x02(\x0e\x32!.fightTheLandlord_poker.CALL_TYPE\x12\x0f\n\x07operate\x18\x03 \x02(\x07\x12\x19\n\x11isConfirmLandlord\x18\x04 \x02(\x08\x12:\n\x0clandlordData\x18\x05 \x01(\x0b\x32$.fightTheLandlord_poker.LandlordData\"n\n\x0cLandlordData\x12\x14\n\x0clandlordSide\x18\x01 \x02(\x07\x12\x11\n\tholeCards\x18\x02 \x02(\t\x12\x11\n\tbaseScore\x18\x03 \x02(\x07\x12\x10\n\x08multiple\x18\x04 \x02(\x07\x12\x10\n\x08wildCard\x18\x05 \x03(\t\"#\n\x0fS_C_SetMultiple\x12\x10\n\x08multiple\x18\x01 \x03(\x07\"G\n\x10S_C_MultipleData\x12\x33\n\x05\x64\x61tas\x18\x01 \x03(\x0b\x32$.fightTheLandlord_poker.MultipleData\".\n\x0cMultipleData\x12\x0c\n\x04side\x18\x01 \x02(\x07\x12\x10\n\x08multiple\x18\x02 \x02(\x07\" \n\x0cS_C_WildCard\x12\x10\n\x08wildCard\x18\x01 \x03(\t\"\x84\x01\n\rS_C_ScoreData\x12\x11\n\tbaseScore\x18\x01 \x02(\x07\x12\x10\n\x08multiple\x18\x02 \x02(\x07\x12\x0e\n\x06isBomb\x18\x03 \x02(\x08\x12>\n\x0eplayerBombData\x18\x04 \x01(\x0b\x32&.fightTheLandlord_poker.PlayerBombData\"\xdd\x02\n\x10S_C_RefreshDatas\x12+\n\x0brefreshData\x18\x01 \x01(\x0b\x32\x16.poker.S_C_RefreshData\x12<\n\x0brobLandlord\x18\x02 \x01(\x0b\x32\'.fightTheLandlord_poker.S_C_RobLandlord\x12:\n\x0clandlordData\x18\x03 \x01(\x0b\x32$.fightTheLandlord_poker.LandlordData\x12>\n\x0eplayerBombData\x18\x04 \x03(\x0b\x32&.fightTheLandlord_poker.PlayerBombData\x12\x0e\n\x06result\x18\x05 \x02(\x08\x12\x0e\n\x06reason\x18\x06 \x01(\t\x12\x42\n\x10lastActionedData\x18\x07 \x03(\x0b\x32(.fightTheLandlord_poker.LastActionedData\"1\n\x0ePlayerBombData\x12\x0c\n\x04side\x18\x01 \x02(\x07\x12\x11\n\tbombCount\x18\x02 \x02(\x07\"j\n\x10LastActionedData\x12\x0c\n\x04side\x18\x01 \x02(\x07\x12\r\n\x05\x63\x61rds\x18\x02 \x01(\t\x12\x10\n\x08\x63\x61llType\x18\x03 \x01(\x07\x12\x10\n\x08\x63\x61llData\x18\x04 \x01(\x07\x12\x15\n\rusedWildCards\x18\x05 \x01(\t*\xce\x01\n\nMSG_HEADER\x12\x13\n\rC_S_OPEN_HAND\x10\x81\xc0\x04\x12\x16\n\x10\x43_S_ROB_LANDLORD\x10\x82\xc0\x04\x12\x13\n\rS_C_OPEN_HAND\x10\x81\xe0\x04\x12\x18\n\x12S_C_OPEN_HAND_DATA\x10\x82\xe0\x04\x12\x16\n\x10S_C_ROB_LANDLORD\x10\x83\xe0\x04\x12\x1d\n\x17S_C_ROB_LANDLORD_RESULT\x10\x84\xe0\x04\x12\x14\n\x0eS_C_SCORE_DATA\x10\x85\xe0\x04\x12\x17\n\x11S_C_REFRESH_DATAS\x10\x86\xe0\x04*@\n\tCALL_TYPE\x12\x11\n\rCALL_LANDLORD\x10\x00\x12\x0e\n\nCALL_SCORE\x10\x01\x12\x10\n\x0cROB_LANDLORD\x10\x02')

_MSG_HEADER = _descriptor.EnumDescriptor(
  name='MSG_HEADER',
  full_name='fightTheLandlord_poker.MSG_HEADER',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='C_S_OPEN_HAND', index=0, number=73729,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='C_S_ROB_LANDLORD', index=1, number=73730,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S_C_OPEN_HAND', index=2, number=77825,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S_C_OPEN_HAND_DATA', index=3, number=77826,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S_C_ROB_LANDLORD', index=4, number=77827,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S_C_ROB_LANDLORD_RESULT', index=5, number=77828,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S_C_SCORE_DATA', index=6, number=77829,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='S_C_REFRESH_DATAS', index=7, number=77830,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1619,
  serialized_end=1825,
)

MSG_HEADER = enum_type_wrapper.EnumTypeWrapper(_MSG_HEADER)
_CALL_TYPE = _descriptor.EnumDescriptor(
  name='CALL_TYPE',
  full_name='fightTheLandlord_poker.CALL_TYPE',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CALL_LANDLORD', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CALL_SCORE', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ROB_LANDLORD', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1827,
  serialized_end=1891,
)

CALL_TYPE = enum_type_wrapper.EnumTypeWrapper(_CALL_TYPE)
C_S_OPEN_HAND = 73729
C_S_ROB_LANDLORD = 73730
S_C_OPEN_HAND = 77825
S_C_OPEN_HAND_DATA = 77826
S_C_ROB_LANDLORD = 77827
S_C_ROB_LANDLORD_RESULT = 77828
S_C_SCORE_DATA = 77829
S_C_REFRESH_DATAS = 77830
CALL_LANDLORD = 0
CALL_SCORE = 1
ROB_LANDLORD = 2



_C_S_OPENHAND = _descriptor.Descriptor(
  name='C_S_OpenHand',
  full_name='fightTheLandlord_poker.C_S_OpenHand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=69,
  serialized_end=83,
)


_C_S_ROBLANDLORD = _descriptor.Descriptor(
  name='C_S_RobLandlord',
  full_name='fightTheLandlord_poker.C_S_RobLandlord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='choseType', full_name='fightTheLandlord_poker.C_S_RobLandlord.choseType', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='operate', full_name='fightTheLandlord_poker.C_S_RobLandlord.operate', index=1,
      number=2, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=85,
  serialized_end=173,
)


_C_S_SETMULTIPLE = _descriptor.Descriptor(
  name='C_S_SetMultiple',
  full_name='fightTheLandlord_poker.C_S_SetMultiple',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='multiple', full_name='fightTheLandlord_poker.C_S_SetMultiple.multiple', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=175,
  serialized_end=210,
)


_S_C_OPENHAND = _descriptor.Descriptor(
  name='S_C_OpenHand',
  full_name='fightTheLandlord_poker.S_C_OpenHand',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=212,
  serialized_end=226,
)


_S_C_OPENHANDDATA = _descriptor.Descriptor(
  name='S_C_OpenHandData',
  full_name='fightTheLandlord_poker.S_C_OpenHandData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='playerHandData', full_name='fightTheLandlord_poker.S_C_OpenHandData.playerHandData', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=228,
  serialized_end=308,
)


_OPENHANDDATA = _descriptor.Descriptor(
  name='OpenHandData',
  full_name='fightTheLandlord_poker.OpenHandData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='side', full_name='fightTheLandlord_poker.OpenHandData.side', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='handCards', full_name='fightTheLandlord_poker.OpenHandData.handCards', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=310,
  serialized_end=357,
)


_S_C_ROBLANDLORD = _descriptor.Descriptor(
  name='S_C_RobLandlord',
  full_name='fightTheLandlord_poker.S_C_RobLandlord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='side', full_name='fightTheLandlord_poker.S_C_RobLandlord.side', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='choseType', full_name='fightTheLandlord_poker.S_C_RobLandlord.choseType', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='canChooseScore', full_name='fightTheLandlord_poker.S_C_RobLandlord.canChooseScore', index=2,
      number=3, type=7, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=359,
  serialized_end=468,
)


_S_C_ROBLANDLORDRESULT = _descriptor.Descriptor(
  name='S_C_RobLandlordResult',
  full_name='fightTheLandlord_poker.S_C_RobLandlordResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='side', full_name='fightTheLandlord_poker.S_C_RobLandlordResult.side', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='choseType', full_name='fightTheLandlord_poker.S_C_RobLandlordResult.choseType', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='operate', full_name='fightTheLandlord_poker.S_C_RobLandlordResult.operate', index=2,
      number=3, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isConfirmLandlord', full_name='fightTheLandlord_poker.S_C_RobLandlordResult.isConfirmLandlord', index=3,
      number=4, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='landlordData', full_name='fightTheLandlord_poker.S_C_RobLandlordResult.landlordData', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=471,
  serialized_end=666,
)


_LANDLORDDATA = _descriptor.Descriptor(
  name='LandlordData',
  full_name='fightTheLandlord_poker.LandlordData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='landlordSide', full_name='fightTheLandlord_poker.LandlordData.landlordSide', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='holeCards', full_name='fightTheLandlord_poker.LandlordData.holeCards', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='baseScore', full_name='fightTheLandlord_poker.LandlordData.baseScore', index=2,
      number=3, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='multiple', full_name='fightTheLandlord_poker.LandlordData.multiple', index=3,
      number=4, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='wildCard', full_name='fightTheLandlord_poker.LandlordData.wildCard', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=668,
  serialized_end=778,
)


_S_C_SETMULTIPLE = _descriptor.Descriptor(
  name='S_C_SetMultiple',
  full_name='fightTheLandlord_poker.S_C_SetMultiple',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='multiple', full_name='fightTheLandlord_poker.S_C_SetMultiple.multiple', index=0,
      number=1, type=7, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=780,
  serialized_end=815,
)


_S_C_MULTIPLEDATA = _descriptor.Descriptor(
  name='S_C_MultipleData',
  full_name='fightTheLandlord_poker.S_C_MultipleData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='datas', full_name='fightTheLandlord_poker.S_C_MultipleData.datas', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=817,
  serialized_end=888,
)


_MULTIPLEDATA = _descriptor.Descriptor(
  name='MultipleData',
  full_name='fightTheLandlord_poker.MultipleData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='side', full_name='fightTheLandlord_poker.MultipleData.side', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='multiple', full_name='fightTheLandlord_poker.MultipleData.multiple', index=1,
      number=2, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=890,
  serialized_end=936,
)


_S_C_WILDCARD = _descriptor.Descriptor(
  name='S_C_WildCard',
  full_name='fightTheLandlord_poker.S_C_WildCard',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='wildCard', full_name='fightTheLandlord_poker.S_C_WildCard.wildCard', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=938,
  serialized_end=970,
)


_S_C_SCOREDATA = _descriptor.Descriptor(
  name='S_C_ScoreData',
  full_name='fightTheLandlord_poker.S_C_ScoreData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='baseScore', full_name='fightTheLandlord_poker.S_C_ScoreData.baseScore', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='multiple', full_name='fightTheLandlord_poker.S_C_ScoreData.multiple', index=1,
      number=2, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='isBomb', full_name='fightTheLandlord_poker.S_C_ScoreData.isBomb', index=2,
      number=3, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='playerBombData', full_name='fightTheLandlord_poker.S_C_ScoreData.playerBombData', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=973,
  serialized_end=1105,
)


_S_C_REFRESHDATAS = _descriptor.Descriptor(
  name='S_C_RefreshDatas',
  full_name='fightTheLandlord_poker.S_C_RefreshDatas',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='refreshData', full_name='fightTheLandlord_poker.S_C_RefreshDatas.refreshData', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='robLandlord', full_name='fightTheLandlord_poker.S_C_RefreshDatas.robLandlord', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='landlordData', full_name='fightTheLandlord_poker.S_C_RefreshDatas.landlordData', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='playerBombData', full_name='fightTheLandlord_poker.S_C_RefreshDatas.playerBombData', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='result', full_name='fightTheLandlord_poker.S_C_RefreshDatas.result', index=4,
      number=5, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='reason', full_name='fightTheLandlord_poker.S_C_RefreshDatas.reason', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lastActionedData', full_name='fightTheLandlord_poker.S_C_RefreshDatas.lastActionedData', index=6,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1108,
  serialized_end=1457,
)


_PLAYERBOMBDATA = _descriptor.Descriptor(
  name='PlayerBombData',
  full_name='fightTheLandlord_poker.PlayerBombData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='side', full_name='fightTheLandlord_poker.PlayerBombData.side', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bombCount', full_name='fightTheLandlord_poker.PlayerBombData.bombCount', index=1,
      number=2, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1459,
  serialized_end=1508,
)


_LASTACTIONEDDATA = _descriptor.Descriptor(
  name='LastActionedData',
  full_name='fightTheLandlord_poker.LastActionedData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='side', full_name='fightTheLandlord_poker.LastActionedData.side', index=0,
      number=1, type=7, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cards', full_name='fightTheLandlord_poker.LastActionedData.cards', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='callType', full_name='fightTheLandlord_poker.LastActionedData.callType', index=2,
      number=3, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='callData', full_name='fightTheLandlord_poker.LastActionedData.callData', index=3,
      number=4, type=7, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='usedWildCards', full_name='fightTheLandlord_poker.LastActionedData.usedWildCards', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1510,
  serialized_end=1616,
)

_C_S_ROBLANDLORD.fields_by_name['choseType'].enum_type = _CALL_TYPE
_S_C_OPENHANDDATA.fields_by_name['playerHandData'].message_type = _OPENHANDDATA
_S_C_ROBLANDLORD.fields_by_name['choseType'].enum_type = _CALL_TYPE
_S_C_ROBLANDLORDRESULT.fields_by_name['choseType'].enum_type = _CALL_TYPE
_S_C_ROBLANDLORDRESULT.fields_by_name['landlordData'].message_type = _LANDLORDDATA
_S_C_MULTIPLEDATA.fields_by_name['datas'].message_type = _MULTIPLEDATA
_S_C_SCOREDATA.fields_by_name['playerBombData'].message_type = _PLAYERBOMBDATA
_S_C_REFRESHDATAS.fields_by_name['refreshData'].message_type = poker_pb2._S_C_REFRESHDATA
_S_C_REFRESHDATAS.fields_by_name['robLandlord'].message_type = _S_C_ROBLANDLORD
_S_C_REFRESHDATAS.fields_by_name['landlordData'].message_type = _LANDLORDDATA
_S_C_REFRESHDATAS.fields_by_name['playerBombData'].message_type = _PLAYERBOMBDATA
_S_C_REFRESHDATAS.fields_by_name['lastActionedData'].message_type = _LASTACTIONEDDATA
DESCRIPTOR.message_types_by_name['C_S_OpenHand'] = _C_S_OPENHAND
DESCRIPTOR.message_types_by_name['C_S_RobLandlord'] = _C_S_ROBLANDLORD
DESCRIPTOR.message_types_by_name['C_S_SetMultiple'] = _C_S_SETMULTIPLE
DESCRIPTOR.message_types_by_name['S_C_OpenHand'] = _S_C_OPENHAND
DESCRIPTOR.message_types_by_name['S_C_OpenHandData'] = _S_C_OPENHANDDATA
DESCRIPTOR.message_types_by_name['OpenHandData'] = _OPENHANDDATA
DESCRIPTOR.message_types_by_name['S_C_RobLandlord'] = _S_C_ROBLANDLORD
DESCRIPTOR.message_types_by_name['S_C_RobLandlordResult'] = _S_C_ROBLANDLORDRESULT
DESCRIPTOR.message_types_by_name['LandlordData'] = _LANDLORDDATA
DESCRIPTOR.message_types_by_name['S_C_SetMultiple'] = _S_C_SETMULTIPLE
DESCRIPTOR.message_types_by_name['S_C_MultipleData'] = _S_C_MULTIPLEDATA
DESCRIPTOR.message_types_by_name['MultipleData'] = _MULTIPLEDATA
DESCRIPTOR.message_types_by_name['S_C_WildCard'] = _S_C_WILDCARD
DESCRIPTOR.message_types_by_name['S_C_ScoreData'] = _S_C_SCOREDATA
DESCRIPTOR.message_types_by_name['S_C_RefreshDatas'] = _S_C_REFRESHDATAS
DESCRIPTOR.message_types_by_name['PlayerBombData'] = _PLAYERBOMBDATA
DESCRIPTOR.message_types_by_name['LastActionedData'] = _LASTACTIONEDDATA

class C_S_OpenHand(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _C_S_OPENHAND

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.C_S_OpenHand)

class C_S_RobLandlord(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _C_S_ROBLANDLORD

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.C_S_RobLandlord)

class C_S_SetMultiple(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _C_S_SETMULTIPLE

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.C_S_SetMultiple)

class S_C_OpenHand(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _S_C_OPENHAND

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.S_C_OpenHand)

class S_C_OpenHandData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _S_C_OPENHANDDATA

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.S_C_OpenHandData)

class OpenHandData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _OPENHANDDATA

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.OpenHandData)

class S_C_RobLandlord(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _S_C_ROBLANDLORD

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.S_C_RobLandlord)

class S_C_RobLandlordResult(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _S_C_ROBLANDLORDRESULT

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.S_C_RobLandlordResult)

class LandlordData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LANDLORDDATA

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.LandlordData)

class S_C_SetMultiple(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _S_C_SETMULTIPLE

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.S_C_SetMultiple)

class S_C_MultipleData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _S_C_MULTIPLEDATA

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.S_C_MultipleData)

class MultipleData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MULTIPLEDATA

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.MultipleData)

class S_C_WildCard(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _S_C_WILDCARD

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.S_C_WildCard)

class S_C_ScoreData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _S_C_SCOREDATA

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.S_C_ScoreData)

class S_C_RefreshDatas(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _S_C_REFRESHDATAS

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.S_C_RefreshDatas)

class PlayerBombData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PLAYERBOMBDATA

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.PlayerBombData)

class LastActionedData(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LASTACTIONEDDATA

  # @@protoc_insertion_point(class_scope:fightTheLandlord_poker.LastActionedData)


# @@protoc_insertion_point(module_scope)

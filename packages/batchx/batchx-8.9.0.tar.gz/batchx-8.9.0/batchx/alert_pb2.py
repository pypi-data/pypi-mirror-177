# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: alert.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x61lert.proto\x12\x0c\x62\x61tchx.alert\x1a\x0c\x63ommon.proto\"\"\n\x13\x44ismissAlertRequest\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x16\n\x14\x44ismissAlertResponse\"\x19\n\x17\x44ismissAllAlertsRequest\"\x1a\n\x18\x44ismissAllAlertsResponse\"\xe1\x07\n\x05\x41lert\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x13\n\x0bts_creation\x18\x02 \x01(\x03\x12&\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x18.batchx.alert.Alert.Data\x1a\x8d\x07\n\x04\x44\x61ta\x12:\n\x0blow_credits\x18\x01 \x01(\x0b\x32#.batchx.alert.Alert.Data.LowCreditsH\x00\x12R\n\x17organization_invitation\x18\x02 \x01(\x0b\x32/.batchx.alert.Alert.Data.OrganizationInvitationH\x00\x12\x39\n\x0bno_jobs_run\x18\x03 \x01(\x0b\x32\".batchx.alert.Alert.Data.NoJobsRunH\x00\x12\x45\n\x11no_files_uploaded\x18\x04 \x01(\x0b\x32(.batchx.alert.Alert.Data.NoFilesUploadedH\x00\x12Q\n\x17no_organization_created\x18\x05 \x01(\x0b\x32..batchx.alert.Alert.Data.NoOrganizationCreatedH\x00\x12<\n\x0cimage_shared\x18\x06 \x01(\x0b\x32$.batchx.alert.Alert.Data.ImageSharedH\x00\x12\x45\n\x11welcome_to_batchx\x18\x07 \x01(\x0b\x32(.batchx.alert.Alert.Data.WelcomeToBatchXH\x00\x1a!\n\nLowCredits\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x1a\x7f\n\x16OrganizationInvitation\x12\x14\n\x0corganization\x18\x01 \x01(\t\x12\n\n\x02\x62y\x18\x02 \x01(\t\x12\x43\n\x04type\x18\x03 \x01(\x0e\x32\x35.batchx.common.Organization.Membership.MembershipType\x1a\x19\n\tNoJobsRun\x12\x0c\n\x04user\x18\x01 \x01(\t\x1a\x1f\n\x0fNoFilesUploaded\x12\x0c\n\x04user\x18\x01 \x01(\t\x1a%\n\x15NoOrganizationCreated\x12\x0c\n\x04user\x18\x01 \x01(\t\x1ak\n\x0bImageShared\x12\x19\n\x11image_environment\x18\x01 \x01(\t\x12\x12\n\nimage_name\x18\x02 \x01(\t\x12\x11\n\tshared_by\x18\x03 \x01(\t\x12\x1a\n\x12target_environment\x18\x04 \x01(\t\x1a\x1f\n\x0fWelcomeToBatchX\x12\x0c\n\x04user\x18\x01 \x01(\tB\x06\n\x04\x43\x61se\"\'\n\x11ListAlertsRequest\x12\x12\n\nreturn_all\x18\x01 \x01(\x08\"8\n\x12ListAlertsResponse\x12\"\n\x05\x61lert\x18\x01 \x03(\x0b\x32\x13.batchx.alert.Alert2\xb6\x02\n\x0c\x41lertService\x12Z\n\x0c\x44ismissAlert\x12!.batchx.alert.DismissAlertRequest\x1a\".batchx.alert.DismissAlertResponse\"\x03\x90\x02\x02\x12\x66\n\x10\x44ismissAllAlerts\x12%.batchx.alert.DismissAllAlertsRequest\x1a&.batchx.alert.DismissAllAlertsResponse\"\x03\x90\x02\x02\x12T\n\nListAlerts\x12\x1f.batchx.alert.ListAlertsRequest\x1a .batchx.alert.ListAlertsResponse\"\x03\x90\x02\x02\x1a\x0c\x82\x97\"\x02\x08\x05\x82\x97\"\x02\x10\x01\x42\x1d\n\x0fio.batchx.protoB\nAlertProtob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'alert_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017io.batchx.protoB\nAlertProto'
  _ALERTSERVICE._options = None
  _ALERTSERVICE._serialized_options = b'\202\227\"\002\010\005\202\227\"\002\020\001'
  _ALERTSERVICE.methods_by_name['DismissAlert']._options = None
  _ALERTSERVICE.methods_by_name['DismissAlert']._serialized_options = b'\220\002\002'
  _ALERTSERVICE.methods_by_name['DismissAllAlerts']._options = None
  _ALERTSERVICE.methods_by_name['DismissAllAlerts']._serialized_options = b'\220\002\002'
  _ALERTSERVICE.methods_by_name['ListAlerts']._options = None
  _ALERTSERVICE.methods_by_name['ListAlerts']._serialized_options = b'\220\002\002'
  _DISMISSALERTREQUEST._serialized_start=43
  _DISMISSALERTREQUEST._serialized_end=77
  _DISMISSALERTRESPONSE._serialized_start=79
  _DISMISSALERTRESPONSE._serialized_end=101
  _DISMISSALLALERTSREQUEST._serialized_start=103
  _DISMISSALLALERTSREQUEST._serialized_end=128
  _DISMISSALLALERTSRESPONSE._serialized_start=130
  _DISMISSALLALERTSRESPONSE._serialized_end=156
  _ALERT._serialized_start=159
  _ALERT._serialized_end=1152
  _ALERT_DATA._serialized_start=243
  _ALERT_DATA._serialized_end=1152
  _ALERT_DATA_LOWCREDITS._serialized_start=741
  _ALERT_DATA_LOWCREDITS._serialized_end=774
  _ALERT_DATA_ORGANIZATIONINVITATION._serialized_start=776
  _ALERT_DATA_ORGANIZATIONINVITATION._serialized_end=903
  _ALERT_DATA_NOJOBSRUN._serialized_start=905
  _ALERT_DATA_NOJOBSRUN._serialized_end=930
  _ALERT_DATA_NOFILESUPLOADED._serialized_start=932
  _ALERT_DATA_NOFILESUPLOADED._serialized_end=963
  _ALERT_DATA_NOORGANIZATIONCREATED._serialized_start=965
  _ALERT_DATA_NOORGANIZATIONCREATED._serialized_end=1002
  _ALERT_DATA_IMAGESHARED._serialized_start=1004
  _ALERT_DATA_IMAGESHARED._serialized_end=1111
  _ALERT_DATA_WELCOMETOBATCHX._serialized_start=1113
  _ALERT_DATA_WELCOMETOBATCHX._serialized_end=1144
  _LISTALERTSREQUEST._serialized_start=1154
  _LISTALERTSREQUEST._serialized_end=1193
  _LISTALERTSRESPONSE._serialized_start=1195
  _LISTALERTSRESPONSE._serialized_end=1251
  _ALERTSERVICE._serialized_start=1254
  _ALERTSERVICE._serialized_end=1564
# @@protoc_insertion_point(module_scope)

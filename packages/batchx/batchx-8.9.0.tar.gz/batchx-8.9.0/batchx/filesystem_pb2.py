# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: filesystem.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import log_pb2 as log__pb2
from . import tag_pb2 as tag__pb2
from . import common_pb2 as common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x66ilesystem.proto\x12\x11\x62\x61tchx.filesystem\x1a\tlog.proto\x1a\ttag.proto\x1a\x0c\x63ommon.proto\"\xa9\x01\n\x10ShareFileRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x1a\n\x12target_environment\x18\x03 \x01(\t\x12\x36\n\x04type\x18\x04 \x01(\x0e\x32(.batchx.filesystem.ShareFileRequest.Type\"\x1e\n\x04Type\x12\t\n\x05SHARE\x10\x00\x12\x0b\n\x07UNSHARE\x10\x01\"\x13\n\x11ShareFileResponse\"j\n\x14SetBlobStatusRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0e\n\x06\x64igest\x18\x02 \x01(\t\x12-\n\x06status\x18\x03 \x01(\x0e\x32\x1d.batchx.filesystem.BlobStatus\"\x17\n\x15SetBlobStatusResponse\"\xad\x05\n\x17ListBlobPointersRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0e\n\x06\x64igest\x18\x02 \x01(\t\x12I\n\npagination\x18\x03 \x01(\x0b\x32\x35.batchx.filesystem.ListBlobPointersRequest.Pagination\x12G\n\tfiltering\x18\x04 \x01(\x0b\x32\x34.batchx.filesystem.ListBlobPointersRequest.Filtering\x12?\n\x05order\x18\x05 \x01(\x0b\x32\x30.batchx.filesystem.ListBlobPointersRequest.Order\x1a\xa3\x01\n\nPagination\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12N\n\x07memento\x18\x02 \x01(\x0b\x32=.batchx.filesystem.ListBlobPointersRequest.Pagination.Memento\x12\x19\n\x11\x63ompute_page_info\x18\x03 \x01(\x08\x1a\x17\n\x07Memento\x12\x0c\n\x04path\x18\x01 \x01(\t\x1aO\n\tFiltering\x12\r\n\x05owner\x18\x01 \x03(\t\x12\x33\n\x0bts_creation\x18\x02 \x01(\x0b\x32\x1e.batchx.common.LongRangeFilter\x1a\xa0\x01\n\x05Order\x12J\n\x08order_by\x18\x01 \x01(\x0e\x32\x38.batchx.filesystem.ListBlobPointersRequest.Order.OrderBy\x12\x11\n\torder_asc\x18\x02 \x01(\x08\x12\x0f\n\x07reverse\x18\x03 \x01(\x08\"\'\n\x07OrderBy\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0f\n\x0bTS_CREATION\x10\x01\"\x8d\x02\n\x18ListBlobPointersResponse\x12%\n\x04\x66ile\x18\x01 \x03(\x0b\x32\x17.batchx.filesystem.File\x12\x11\n\tlast_page\x18\x02 \x01(\x08\x12G\n\x06owners\x18\x03 \x03(\x0b\x32\x37.batchx.filesystem.ListBlobPointersResponse.OwnersEntry\x12*\n\tpage_info\x18\x04 \x01(\x0b\x32\x17.batchx.common.PageInfo\x1a\x42\n\x0bOwnersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.batchx.common.User:\x02\x38\x01\"\xf4\x06\n\x10ListBlobsRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x38\n\x05order\x18\x02 \x01(\x0b\x32).batchx.filesystem.ListBlobsRequest.Order\x12\x42\n\npagination\x18\x03 \x01(\x0b\x32..batchx.filesystem.ListBlobsRequest.Pagination\x12@\n\tfiltering\x18\x04 \x01(\x0b\x32-.batchx.filesystem.ListBlobsRequest.Filtering\x1a\xc9\x01\n\x05Order\x12\x43\n\x08order_by\x18\x01 \x01(\x0e\x32\x31.batchx.filesystem.ListBlobsRequest.Order.OrderBy\x12\x11\n\torder_asc\x18\x02 \x01(\x08\x12\x0f\n\x07reverse\x18\x03 \x01(\x08\"W\n\x07OrderBy\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0c\n\x08POINTERS\x10\x01\x12\n\n\x06LENGTH\x10\x02\x12\x0f\n\x0bTS_CREATION\x10\x03\x12\x14\n\x10TS_LAST_MODIFIED\x10\x04\x1a\x9e\x01\n\nPagination\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12G\n\x07memento\x18\x02 \x01(\x0b\x32\x36.batchx.filesystem.ListBlobsRequest.Pagination.Memento\x12\x19\n\x11\x63ompute_page_info\x18\x03 \x01(\x08\x1a\x19\n\x07Memento\x12\x0e\n\x06\x64igest\x18\x01 \x01(\t\x1a\x9d\x02\n\tFiltering\x12\x0c\n\x04user\x18\x01 \x03(\t\x12/\n\x08pointers\x18\x02 \x01(\x0b\x32\x1d.batchx.common.IntRangeFilter\x12.\n\x06length\x18\x03 \x01(\x0b\x32\x1e.batchx.common.LongRangeFilter\x12\x33\n\x0bts_creation\x18\x04 \x01(\x0b\x32\x1e.batchx.common.LongRangeFilter\x12\x38\n\x10ts_last_modified\x18\x05 \x01(\x0b\x32\x1e.batchx.common.LongRangeFilter\x12\x32\n\x0b\x62lob_status\x18\x06 \x03(\x0e\x32\x1d.batchx.filesystem.BlobStatus\"\xfc\x01\n\x11ListBlobsResponse\x12%\n\x04\x62lob\x18\x01 \x03(\x0b\x32\x17.batchx.filesystem.Blob\x12\x11\n\tlast_page\x18\x02 \x01(\x08\x12>\n\x05users\x18\x03 \x03(\x0b\x32/.batchx.filesystem.ListBlobsResponse.UsersEntry\x12*\n\tpage_info\x18\x04 \x01(\x0b\x32\x17.batchx.common.PageInfo\x1a\x41\n\nUsersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.batchx.common.User:\x02\x38\x01\"5\n\x0eGetBlobRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0e\n\x06\x64igest\x18\x02 \x01(\t\"8\n\x0fGetBlobResponse\x12%\n\x04\x62lob\x18\x01 \x01(\x0b\x32\x17.batchx.filesystem.Blob\"\xf6\x02\n\x04\x42lob\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0e\n\x06\x64igest\x18\x02 \x01(\t\x12\x10\n\x08pointers\x18\x03 \x01(\x05\x12\x0e\n\x06length\x18\x04 \x01(\x03\x12\x13\n\x0bts_creation\x18\x05 \x01(\x03\x12\x18\n\x10ts_last_modified\x18\x06 \x01(\x03\x12\x0c\n\x04user\x18\x07 \x01(\t\x12\x15\n\roriginal_path\x18\x08 \x01(\t\x12-\n\x06status\x18\t \x01(\x0e\x32\x1d.batchx.filesystem.BlobStatus\x12\x16\n\x0ets_archivation\x18\n \x01(\x03\x12\x33\n\tmeta_info\x18\x0b \x01(\x0b\x32 .batchx.filesystem.Blob.MetaInfo\x1aW\n\x08MetaInfo\x12\x0e\n\x06\x62inary\x18\x01 \x01(\x08\x12\x0c\n\x04gzip\x18\x02 \x01(\x08\x12\x19\n\x11\x64\x65\x63ompressed_size\x18\x03 \x01(\x03\x12\x12\n\nline_count\x18\x04 \x01(\x03\"\x82\x08\n\x11ListFolderRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x11\n\trecursive\x18\x03 \x01(\x08\x12\x41\n\tfiltering\x18\x04 \x01(\x0b\x32..batchx.filesystem.ListFolderRequest.Filtering\x12\x43\n\npagination\x18\x05 \x01(\x0b\x32/.batchx.filesystem.ListFolderRequest.Pagination\x12\x39\n\x05order\x18\x06 \x01(\x0b\x32*.batchx.filesystem.ListFolderRequest.Order\x12\x18\n\x10user_environment\x18\x07 \x01(\t\x1a\xe2\x02\n\tFiltering\x12\x0c\n\x04user\x18\x01 \x03(\t\x12\x12\n\nonly_ready\x18\x02 \x01(\x08\x12\x17\n\rexclude_files\x18\x03 \x01(\x08H\x00\x12\x19\n\x0f\x65xclude_folders\x18\x04 \x01(\x08H\x00\x12\'\n\x03tag\x18\x05 \x03(\x0b\x32\x1a.batchx.tag.TagCoordinates\x12\x33\n\x0bts_creation\x18\x06 \x01(\x0b\x32\x1e.batchx.common.LongRangeFilter\x12\x38\n\x10ts_last_modified\x18\x07 \x01(\x0b\x32\x1e.batchx.common.LongRangeFilter\x12.\n\x06length\x18\x08 \x01(\x0b\x32\x1e.batchx.common.LongRangeFilter\x12/\n\x08pointers\x18\t \x01(\x0b\x32\x1d.batchx.common.IntRangeFilterB\x06\n\x04Type\x1a\x9d\x01\n\nPagination\x12\x11\n\tpage_size\x18\x01 \x01(\x05\x12H\n\x07memento\x18\x02 \x01(\x0b\x32\x37.batchx.filesystem.ListFolderRequest.Pagination.Memento\x12\x19\n\x11\x63ompute_page_info\x18\x03 \x01(\x08\x1a\x17\n\x07Memento\x12\x0c\n\x04path\x18\x01 \x01(\t\x1a\xd4\x01\n\x05Order\x12\x44\n\x08order_by\x18\x01 \x01(\x0e\x32\x32.batchx.filesystem.ListFolderRequest.Order.OrderBy\x12\x11\n\torder_asc\x18\x02 \x01(\x08\x12\x0f\n\x07reverse\x18\x03 \x01(\x08\"a\n\x07OrderBy\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x08\n\x04PATH\x10\x01\x12\n\n\x06LENGTH\x10\x02\x12\x0f\n\x0bTS_CREATION\x10\x03\x12\x14\n\x10TS_LAST_MODIFIED\x10\x04\x12\x0c\n\x08POINTERS\x10\x05\"\x87\x02\n\x12ListFolderResponse\x12%\n\x04\x66ile\x18\x01 \x03(\x0b\x32\x17.batchx.filesystem.File\x12\x11\n\tlast_page\x18\x02 \x01(\x08\x12\x41\n\x06owners\x18\x04 \x03(\x0b\x32\x31.batchx.filesystem.ListFolderResponse.OwnersEntry\x12*\n\tpage_info\x18\x05 \x01(\x0b\x32\x17.batchx.common.PageInfo\x1a\x42\n\x0bOwnersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.batchx.common.User:\x02\x38\x01J\x04\x08\x03\x10\x04\"\xb2\x01\n\x13\x43reateFolderRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12G\n\tuser_data\x18\x03 \x03(\x0b\x32\x34.batchx.filesystem.CreateFolderRequest.UserDataEntry\x1a/\n\rUserDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x16\n\x14\x43reateFolderResponse\"8\n\x13\x44\x65leteFolderRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"\x16\n\x14\x44\x65leteFolderResponse\"6\n\x11\x44\x65leteFileRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"8\n\x12\x44\x65leteFileResponse\x12\x0e\n\x06\x64igest\x18\x01 \x01(\t\x12\x12\n\nother_refs\x18\x02 \x01(\x05\"3\n\x0eGetFileRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"b\n\x0fGetFileResponse\x12%\n\x04\x66ile\x18\x01 \x01(\x0b\x32\x17.batchx.filesystem.File\x12\"\n\x05owner\x18\x03 \x01(\x0b\x32\x13.batchx.common.UserJ\x04\x08\x02\x10\x03\"\xe4\x02\n\x04\x46ile\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x0e\n\x06\x66older\x18\x03 \x01(\x08\x12-\n\x08metadata\x18\x04 \x01(\x0b\x32\x1b.batchx.filesystem.Metadata\x12\x13\n\x0bts_creation\x18\x05 \x01(\x03\x12\x18\n\x10ts_last_modified\x18\x06 \x01(\x03\x12\r\n\x05owner\x18\x07 \x01(\t\x12.\n\x06status\x18\x08 \x01(\x0e\x32\x1e.batchx.filesystem.File.Status\x12\x10\n\x08pointers\x18\t \x01(\x05\x12\x32\n\x0b\x62lob_status\x18\n \x01(\x0e\x32\x1d.batchx.filesystem.BlobStatus\x12\x13\n\x0bshared_with\x18\x0b \x03(\t\"1\n\x06Status\x12\t\n\x05READY\x10\x00\x12\r\n\tUPLOADING\x10\x01\x12\r\n\tIMPORTING\x10\x02\"V\n\x19ReportUploadStatusRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x16\n\x0euploaded_bytes\x18\x03 \x01(\x03\"\x1c\n\x1aReportUploadStatusResponse\"8\n\x13\x43\x61ncelUploadRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"\x16\n\x14\x43\x61ncelUploadResponse\"\xe8\x01\n\x08Metadata\x12\x0e\n\x06length\x18\x01 \x01(\x03\x12\x0e\n\x06\x64igest\x18\x02 \x01(\t\x12<\n\tuser_data\x18\x03 \x03(\x0b\x32).batchx.filesystem.Metadata.UserDataEntry\x12\x13\n\x0bpart_length\x18\x04 \x01(\x03\x12\x38\n\x0e\x62lob_meta_info\x18\x05 \x01(\x0b\x32 .batchx.filesystem.Blob.MetaInfo\x1a/\n\rUserDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"j\n\x16UploadPresignedRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12-\n\x08metadata\x18\x03 \x01(\x0b\x32\x1b.batchx.filesystem.Metadata\"\xa0\x01\n\x17UploadPresignedResponse\x12\x1a\n\x10\x61lready_uploaded\x18\x01 \x01(\x08H\x00\x12H\n\tpart_urls\x18\x02 \x01(\x0b\x32\x33.batchx.filesystem.UploadPresignedResponse.PartUrlsH\x00\x1a\x17\n\x08PartUrls\x12\x0b\n\x03url\x18\x01 \x03(\tB\x06\n\x04\x43\x61se\"h\n\x18\x44ownloadPresignedRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\r\n\x05range\x18\x03 \x01(\t\x12\x0e\n\x04path\x18\x02 \x01(\tH\x00\x12\x10\n\x06\x64igest\x18\x04 \x01(\tH\x00\x42\x06\n\x04\x43\x61se\"W\n\x19\x44ownloadPresignedResponse\x12\x0b\n\x03url\x18\x01 \x01(\t\x12-\n\x08metadata\x18\x02 \x01(\x0b\x32\x1b.batchx.filesystem.Metadata\"o\n\x0b\x43opyRequest\x12\x1a\n\x12source_environment\x18\x01 \x01(\t\x12\x13\n\x0bsource_path\x18\x02 \x01(\t\x12\x1a\n\x12target_environment\x18\x03 \x01(\t\x12\x13\n\x0btarget_path\x18\x04 \x01(\t\"L\n\x15\x43ompleteUploadRequest\x12\x13\n\x0b\x65nvironment\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\x12\x10\n\x08part_md5\x18\x03 \x03(\t\"\x18\n\x16\x43ompleteUploadResponse*x\n\nBlobStatus\x12\x08\n\x04LIVE\x10\x00\x12\x15\n\x11LIVE_AND_ARCHIVED\x10\x01\x12\x0c\n\x08\x41RCHIVED\x10\x02\x12\r\n\tARCHIVING\x10\n\x12\x0c\n\x08UNLIVING\x10\x0b\x12\r\n\tRESTORING\x10\x0c\x12\x0f\n\x0bUNARCHIVING\x10\r2\xc0\x0b\n\x11\x46ilesystemService\x12U\n\x07GetFile\x12!.batchx.filesystem.GetFileRequest\x1a\".batchx.filesystem.GetFileResponse\"\x03\x90\x02\x01\x12m\n\x0fUploadPresigned\x12).batchx.filesystem.UploadPresignedRequest\x1a*.batchx.filesystem.UploadPresignedResponse\"\x03\x90\x02\x02\x12v\n\x12ReportUploadStatus\x12,.batchx.filesystem.ReportUploadStatusRequest\x1a-.batchx.filesystem.ReportUploadStatusResponse\"\x03\x90\x02\x02\x12\x64\n\x0c\x43\x61ncelUpload\x12&.batchx.filesystem.CancelUploadRequest\x1a\'.batchx.filesystem.CancelUploadResponse\"\x03\x90\x02\x01\x12n\n\x0e\x43ompleteUpload\x12(.batchx.filesystem.CompleteUploadRequest\x1a).batchx.filesystem.CompleteUploadResponse\"\x07\x90\x02\x02\x88\xa6\x1d\x02\x12s\n\x11\x44ownloadPresigned\x12+.batchx.filesystem.DownloadPresignedRequest\x1a,.batchx.filesystem.DownloadPresignedResponse\"\x03\x90\x02\x02\x12^\n\nDeleteFile\x12$.batchx.filesystem.DeleteFileRequest\x1a%.batchx.filesystem.DeleteFileResponse\"\x03\x90\x02\x02\x12j\n\nListFolder\x12$.batchx.filesystem.ListFolderRequest\x1a%.batchx.filesystem.ListFolderResponse\"\x0f\x90\x02\x01\x82\xa6\x1d\x02\x08\x05\x82\xa6\x1d\x02\x10\x01\x12g\n\tListBlobs\x12#.batchx.filesystem.ListBlobsRequest\x1a$.batchx.filesystem.ListBlobsResponse\"\x0f\x90\x02\x01\x82\xa6\x1d\x02\x08\x05\x82\xa6\x1d\x02\x10\x01\x12U\n\x07GetBlob\x12!.batchx.filesystem.GetBlobRequest\x1a\".batchx.filesystem.GetBlobResponse\"\x03\x90\x02\x01\x12g\n\rSetBlobStatus\x12\'.batchx.filesystem.SetBlobStatusRequest\x1a(.batchx.filesystem.SetBlobStatusResponse\"\x03\x90\x02\x01\x12|\n\x10ListBlobPointers\x12*.batchx.filesystem.ListBlobPointersRequest\x1a+.batchx.filesystem.ListBlobPointersResponse\"\x0f\x90\x02\x01\x82\xa6\x1d\x02\x08\x05\x82\xa6\x1d\x02\x10\x01\x12\x44\n\x04\x43opy\x12\x1e.batchx.filesystem.CopyRequest\x1a\x15.batchx.log.LogRecord\"\x03\x90\x02\x02\x30\x01\x12[\n\tShareFile\x12#.batchx.filesystem.ShareFileRequest\x1a$.batchx.filesystem.ShareFileResponse\"\x03\x90\x02\x02\x1a\x0c\x82\x97\"\x02\x08\x32\x82\x97\"\x02\x10\x01\x42\"\n\x0fio.batchx.protoB\x0f\x46ilesystemProtob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'filesystem_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\017io.batchx.protoB\017FilesystemProto'
  _LISTBLOBPOINTERSRESPONSE_OWNERSENTRY._options = None
  _LISTBLOBPOINTERSRESPONSE_OWNERSENTRY._serialized_options = b'8\001'
  _LISTBLOBSRESPONSE_USERSENTRY._options = None
  _LISTBLOBSRESPONSE_USERSENTRY._serialized_options = b'8\001'
  _LISTFOLDERRESPONSE_OWNERSENTRY._options = None
  _LISTFOLDERRESPONSE_OWNERSENTRY._serialized_options = b'8\001'
  _CREATEFOLDERREQUEST_USERDATAENTRY._options = None
  _CREATEFOLDERREQUEST_USERDATAENTRY._serialized_options = b'8\001'
  _METADATA_USERDATAENTRY._options = None
  _METADATA_USERDATAENTRY._serialized_options = b'8\001'
  _FILESYSTEMSERVICE._options = None
  _FILESYSTEMSERVICE._serialized_options = b'\202\227\"\002\0102\202\227\"\002\020\001'
  _FILESYSTEMSERVICE.methods_by_name['GetFile']._options = None
  _FILESYSTEMSERVICE.methods_by_name['GetFile']._serialized_options = b'\220\002\001'
  _FILESYSTEMSERVICE.methods_by_name['UploadPresigned']._options = None
  _FILESYSTEMSERVICE.methods_by_name['UploadPresigned']._serialized_options = b'\220\002\002'
  _FILESYSTEMSERVICE.methods_by_name['ReportUploadStatus']._options = None
  _FILESYSTEMSERVICE.methods_by_name['ReportUploadStatus']._serialized_options = b'\220\002\002'
  _FILESYSTEMSERVICE.methods_by_name['CancelUpload']._options = None
  _FILESYSTEMSERVICE.methods_by_name['CancelUpload']._serialized_options = b'\220\002\001'
  _FILESYSTEMSERVICE.methods_by_name['CompleteUpload']._options = None
  _FILESYSTEMSERVICE.methods_by_name['CompleteUpload']._serialized_options = b'\220\002\002\210\246\035\002'
  _FILESYSTEMSERVICE.methods_by_name['DownloadPresigned']._options = None
  _FILESYSTEMSERVICE.methods_by_name['DownloadPresigned']._serialized_options = b'\220\002\002'
  _FILESYSTEMSERVICE.methods_by_name['DeleteFile']._options = None
  _FILESYSTEMSERVICE.methods_by_name['DeleteFile']._serialized_options = b'\220\002\002'
  _FILESYSTEMSERVICE.methods_by_name['ListFolder']._options = None
  _FILESYSTEMSERVICE.methods_by_name['ListFolder']._serialized_options = b'\220\002\001\202\246\035\002\010\005\202\246\035\002\020\001'
  _FILESYSTEMSERVICE.methods_by_name['ListBlobs']._options = None
  _FILESYSTEMSERVICE.methods_by_name['ListBlobs']._serialized_options = b'\220\002\001\202\246\035\002\010\005\202\246\035\002\020\001'
  _FILESYSTEMSERVICE.methods_by_name['GetBlob']._options = None
  _FILESYSTEMSERVICE.methods_by_name['GetBlob']._serialized_options = b'\220\002\001'
  _FILESYSTEMSERVICE.methods_by_name['SetBlobStatus']._options = None
  _FILESYSTEMSERVICE.methods_by_name['SetBlobStatus']._serialized_options = b'\220\002\001'
  _FILESYSTEMSERVICE.methods_by_name['ListBlobPointers']._options = None
  _FILESYSTEMSERVICE.methods_by_name['ListBlobPointers']._serialized_options = b'\220\002\001\202\246\035\002\010\005\202\246\035\002\020\001'
  _FILESYSTEMSERVICE.methods_by_name['Copy']._options = None
  _FILESYSTEMSERVICE.methods_by_name['Copy']._serialized_options = b'\220\002\002'
  _FILESYSTEMSERVICE.methods_by_name['ShareFile']._options = None
  _FILESYSTEMSERVICE.methods_by_name['ShareFile']._serialized_options = b'\220\002\002'
  _BLOBSTATUS._serialized_start=6319
  _BLOBSTATUS._serialized_end=6439
  _SHAREFILEREQUEST._serialized_start=76
  _SHAREFILEREQUEST._serialized_end=245
  _SHAREFILEREQUEST_TYPE._serialized_start=215
  _SHAREFILEREQUEST_TYPE._serialized_end=245
  _SHAREFILERESPONSE._serialized_start=247
  _SHAREFILERESPONSE._serialized_end=266
  _SETBLOBSTATUSREQUEST._serialized_start=268
  _SETBLOBSTATUSREQUEST._serialized_end=374
  _SETBLOBSTATUSRESPONSE._serialized_start=376
  _SETBLOBSTATUSRESPONSE._serialized_end=399
  _LISTBLOBPOINTERSREQUEST._serialized_start=402
  _LISTBLOBPOINTERSREQUEST._serialized_end=1087
  _LISTBLOBPOINTERSREQUEST_PAGINATION._serialized_start=680
  _LISTBLOBPOINTERSREQUEST_PAGINATION._serialized_end=843
  _LISTBLOBPOINTERSREQUEST_PAGINATION_MEMENTO._serialized_start=820
  _LISTBLOBPOINTERSREQUEST_PAGINATION_MEMENTO._serialized_end=843
  _LISTBLOBPOINTERSREQUEST_FILTERING._serialized_start=845
  _LISTBLOBPOINTERSREQUEST_FILTERING._serialized_end=924
  _LISTBLOBPOINTERSREQUEST_ORDER._serialized_start=927
  _LISTBLOBPOINTERSREQUEST_ORDER._serialized_end=1087
  _LISTBLOBPOINTERSREQUEST_ORDER_ORDERBY._serialized_start=1048
  _LISTBLOBPOINTERSREQUEST_ORDER_ORDERBY._serialized_end=1087
  _LISTBLOBPOINTERSRESPONSE._serialized_start=1090
  _LISTBLOBPOINTERSRESPONSE._serialized_end=1359
  _LISTBLOBPOINTERSRESPONSE_OWNERSENTRY._serialized_start=1293
  _LISTBLOBPOINTERSRESPONSE_OWNERSENTRY._serialized_end=1359
  _LISTBLOBSREQUEST._serialized_start=1362
  _LISTBLOBSREQUEST._serialized_end=2246
  _LISTBLOBSREQUEST_ORDER._serialized_start=1596
  _LISTBLOBSREQUEST_ORDER._serialized_end=1797
  _LISTBLOBSREQUEST_ORDER_ORDERBY._serialized_start=1710
  _LISTBLOBSREQUEST_ORDER_ORDERBY._serialized_end=1797
  _LISTBLOBSREQUEST_PAGINATION._serialized_start=1800
  _LISTBLOBSREQUEST_PAGINATION._serialized_end=1958
  _LISTBLOBSREQUEST_PAGINATION_MEMENTO._serialized_start=1933
  _LISTBLOBSREQUEST_PAGINATION_MEMENTO._serialized_end=1958
  _LISTBLOBSREQUEST_FILTERING._serialized_start=1961
  _LISTBLOBSREQUEST_FILTERING._serialized_end=2246
  _LISTBLOBSRESPONSE._serialized_start=2249
  _LISTBLOBSRESPONSE._serialized_end=2501
  _LISTBLOBSRESPONSE_USERSENTRY._serialized_start=2436
  _LISTBLOBSRESPONSE_USERSENTRY._serialized_end=2501
  _GETBLOBREQUEST._serialized_start=2503
  _GETBLOBREQUEST._serialized_end=2556
  _GETBLOBRESPONSE._serialized_start=2558
  _GETBLOBRESPONSE._serialized_end=2614
  _BLOB._serialized_start=2617
  _BLOB._serialized_end=2991
  _BLOB_METAINFO._serialized_start=2904
  _BLOB_METAINFO._serialized_end=2991
  _LISTFOLDERREQUEST._serialized_start=2994
  _LISTFOLDERREQUEST._serialized_end=4020
  _LISTFOLDERREQUEST_FILTERING._serialized_start=3291
  _LISTFOLDERREQUEST_FILTERING._serialized_end=3645
  _LISTFOLDERREQUEST_PAGINATION._serialized_start=3648
  _LISTFOLDERREQUEST_PAGINATION._serialized_end=3805
  _LISTFOLDERREQUEST_PAGINATION_MEMENTO._serialized_start=820
  _LISTFOLDERREQUEST_PAGINATION_MEMENTO._serialized_end=843
  _LISTFOLDERREQUEST_ORDER._serialized_start=3808
  _LISTFOLDERREQUEST_ORDER._serialized_end=4020
  _LISTFOLDERREQUEST_ORDER_ORDERBY._serialized_start=3923
  _LISTFOLDERREQUEST_ORDER_ORDERBY._serialized_end=4020
  _LISTFOLDERRESPONSE._serialized_start=4023
  _LISTFOLDERRESPONSE._serialized_end=4286
  _LISTFOLDERRESPONSE_OWNERSENTRY._serialized_start=1293
  _LISTFOLDERRESPONSE_OWNERSENTRY._serialized_end=1359
  _CREATEFOLDERREQUEST._serialized_start=4289
  _CREATEFOLDERREQUEST._serialized_end=4467
  _CREATEFOLDERREQUEST_USERDATAENTRY._serialized_start=4420
  _CREATEFOLDERREQUEST_USERDATAENTRY._serialized_end=4467
  _CREATEFOLDERRESPONSE._serialized_start=4469
  _CREATEFOLDERRESPONSE._serialized_end=4491
  _DELETEFOLDERREQUEST._serialized_start=4493
  _DELETEFOLDERREQUEST._serialized_end=4549
  _DELETEFOLDERRESPONSE._serialized_start=4551
  _DELETEFOLDERRESPONSE._serialized_end=4573
  _DELETEFILEREQUEST._serialized_start=4575
  _DELETEFILEREQUEST._serialized_end=4629
  _DELETEFILERESPONSE._serialized_start=4631
  _DELETEFILERESPONSE._serialized_end=4687
  _GETFILEREQUEST._serialized_start=4689
  _GETFILEREQUEST._serialized_end=4740
  _GETFILERESPONSE._serialized_start=4742
  _GETFILERESPONSE._serialized_end=4840
  _FILE._serialized_start=4843
  _FILE._serialized_end=5199
  _FILE_STATUS._serialized_start=5150
  _FILE_STATUS._serialized_end=5199
  _REPORTUPLOADSTATUSREQUEST._serialized_start=5201
  _REPORTUPLOADSTATUSREQUEST._serialized_end=5287
  _REPORTUPLOADSTATUSRESPONSE._serialized_start=5289
  _REPORTUPLOADSTATUSRESPONSE._serialized_end=5317
  _CANCELUPLOADREQUEST._serialized_start=5319
  _CANCELUPLOADREQUEST._serialized_end=5375
  _CANCELUPLOADRESPONSE._serialized_start=5377
  _CANCELUPLOADRESPONSE._serialized_end=5399
  _METADATA._serialized_start=5402
  _METADATA._serialized_end=5634
  _METADATA_USERDATAENTRY._serialized_start=4420
  _METADATA_USERDATAENTRY._serialized_end=4467
  _UPLOADPRESIGNEDREQUEST._serialized_start=5636
  _UPLOADPRESIGNEDREQUEST._serialized_end=5742
  _UPLOADPRESIGNEDRESPONSE._serialized_start=5745
  _UPLOADPRESIGNEDRESPONSE._serialized_end=5905
  _UPLOADPRESIGNEDRESPONSE_PARTURLS._serialized_start=5874
  _UPLOADPRESIGNEDRESPONSE_PARTURLS._serialized_end=5897
  _DOWNLOADPRESIGNEDREQUEST._serialized_start=5907
  _DOWNLOADPRESIGNEDREQUEST._serialized_end=6011
  _DOWNLOADPRESIGNEDRESPONSE._serialized_start=6013
  _DOWNLOADPRESIGNEDRESPONSE._serialized_end=6100
  _COPYREQUEST._serialized_start=6102
  _COPYREQUEST._serialized_end=6213
  _COMPLETEUPLOADREQUEST._serialized_start=6215
  _COMPLETEUPLOADREQUEST._serialized_end=6291
  _COMPLETEUPLOADRESPONSE._serialized_start=6293
  _COMPLETEUPLOADRESPONSE._serialized_end=6317
  _FILESYSTEMSERVICE._serialized_start=6442
  _FILESYSTEMSERVICE._serialized_end=7914
# @@protoc_insertion_point(module_scope)

import 'dart:async';

import '/backend/schema/util/firestore_util.dart';
import '/backend/schema/util/schema_util.dart';

import 'index.dart';
import '/flutter_flow/flutter_flow_util.dart';

class StatusRecord extends FirestoreRecord {
  StatusRecord._(
    DocumentReference reference,
    Map<String, dynamic> data,
  ) : super(reference, data) {
    _initializeFields();
  }

  // "status_sids" field.
  bool? _statusSids;
  bool get statusSids => _statusSids ?? false;
  bool hasStatusSids() => _statusSids != null;

  void _initializeFields() {
    _statusSids = snapshotData['status_sids'] as bool?;
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('status');

  static Stream<StatusRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => StatusRecord.fromSnapshot(s));

  static Future<StatusRecord> getDocumentOnce(DocumentReference ref) =>
      ref.get().then((s) => StatusRecord.fromSnapshot(s));

  static StatusRecord fromSnapshot(DocumentSnapshot snapshot) => StatusRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static StatusRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      StatusRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'StatusRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is StatusRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createStatusRecordData({
  bool? statusSids,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'status_sids': statusSids,
    }.withoutNulls,
  );

  return firestoreData;
}

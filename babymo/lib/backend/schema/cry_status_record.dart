import 'dart:async';

import '/backend/schema/util/firestore_util.dart';
import '/backend/schema/util/schema_util.dart';

import 'index.dart';
import '/flutter_flow/flutter_flow_util.dart';

class CryStatusRecord extends FirestoreRecord {
  CryStatusRecord._(
    DocumentReference reference,
    Map<String, dynamic> data,
  ) : super(reference, data) {
    _initializeFields();
  }

  // "status_cry" field.
  bool? _statusCry;
  bool get statusCry => _statusCry ?? false;
  bool hasStatusCry() => _statusCry != null;

  void _initializeFields() {
    _statusCry = snapshotData['status_cry'] as bool?;
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('cry_status');

  static Stream<CryStatusRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => CryStatusRecord.fromSnapshot(s));

  static Future<CryStatusRecord> getDocumentOnce(DocumentReference ref) =>
      ref.get().then((s) => CryStatusRecord.fromSnapshot(s));

  static CryStatusRecord fromSnapshot(DocumentSnapshot snapshot) =>
      CryStatusRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static CryStatusRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      CryStatusRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'CryStatusRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is CryStatusRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createCryStatusRecordData({
  bool? statusCry,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'status_cry': statusCry,
    }.withoutNulls,
  );

  return firestoreData;
}

import '/auth/firebase_auth/auth_util.dart';
import '/backend/backend.dart';
import '/flutter_flow/flutter_flow_icon_button.dart';
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import '/flutter_flow/flutter_flow_widgets.dart';
import '/flutter_flow/instant_timer.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

class DangerModel extends FlutterFlowModel {
  ///  Local state fields for this page.

  String? text = 'textstatus';

  Color? colors = const Color(0xFFFF0000);

  ///  State fields for stateful widgets in this page.

  InstantTimer? instantTimerdanger;
  // Stores action output result for [Firestore Query - Query a collection] action in Danger widget.
  StatusRecord? crystatusdanger;

  /// Initialization and disposal methods.

  void initState(BuildContext context) {}

  void dispose() {
    instantTimerdanger?.cancel();
  }

  /// Action blocks are added here.

  /// Additional helper methods are added here.
}

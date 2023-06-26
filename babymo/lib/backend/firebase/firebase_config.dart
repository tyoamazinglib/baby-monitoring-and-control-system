import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: FirebaseOptions(
            apiKey: "AIzaSyDTKYmbEAKIiYtzdJFKPji0MxriVFatMgs",
            authDomain: "babymo.firebaseapp.com",
            projectId: "babymo",
            storageBucket: "babymo.appspot.com",
            messagingSenderId: "469541110958",
            appId: "1:469541110958:web:d981e1262b174b3e69993f"));
  } else {
    await Firebase.initializeApp();
  }
}

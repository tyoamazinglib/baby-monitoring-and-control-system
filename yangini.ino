#include <WiFi.h>
#include <FirebaseESP32.h>
#include <DFRobotDFPlayerMini.h>

// Masukkan informasi WiFi dan Firebase
#define WIFI_SSID "Gunawan's inn"
#define WIFI_PASSWORD "Daffa2001"
#define FIREBASE_HOST "iot-water-ionizer-default-rtdb.firebaseio.com/"
#define FIREBASE_AUTH "AIzaSyAeXAF7Mfu4WwAz-sydwYh96QsdvGLK-Kw"

FirebaseData firebaseData;

// Inisialisasi objek MP3
SoftwareSerial mp3Serial(16, 17);
HardwareSerial mySoftwareSerial(1);
DFRobotDFPlayerMini mp3Player;

void setup() {
  Serial.begin(115200);

  // Mulai koneksi WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
    delay(1000);
  }

  // Mulai koneksi Firebase
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

  // Mulai koneksi MP3
  mp3Serial.begin(9600);
  mp3Player.begin(mp3Serial);

  // Mengatur volume MP3 menjadi maksimum
  mp3Player.volume(30);
}

void loop() {
  // Baca keputusan dari Firebase
  if (Firebase.getString(firebaseData, "/path/to/decision")) {
    String tds = firebaseData.stringData();

    // Jika keputusan adalah "play", putar lagu
    if (tds == 0) {
      mp3Player.play(1); // nomor lagu yang akan diputar
    }
    if (tds > 1000 ){
      mp3Player.play(2);
    }
  } else {
    Serial.println(firebaseData.errorReason());
  }

  delay(1000);
}

//belum final, keknya bakal gua rombak ulang aja

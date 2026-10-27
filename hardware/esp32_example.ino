// Optional ESP32 prototype example for a local test bench.
// This does not control live traffic infrastructure.

const char *ssid = "AELMS_TEST_WIFI";
const char *password = "test-password";

void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  Serial.println("AELMS ESP32 demo ready. Simulation only.");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "GREEN") {
      digitalWrite(2, HIGH);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
    } else if (command == "YELLOW") {
      digitalWrite(2, LOW);
      digitalWrite(4, HIGH);
      digitalWrite(5, LOW);
    } else if (command == "RED") {
      digitalWrite(2, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, HIGH);
    }
  }
}

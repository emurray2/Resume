int flex = A0;
int flex_data = 0;
int trigPin = 11;
int echoPin = 12;
long duration, cm, inches;
void setup() {
  Serial.begin(9600);
  // Set the pins for each of the sensors
  pinMode(flex, INPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Control write and read
  digitalWrite(trigPin, LOW);
  delayMicroseconds(5);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
  // Get the cm from the ultrasonic sensor
  cm = (duration/2) / 29.1;
  // Get the data from the flex sensor
  flex_data = analogRead(flex);
  Serial.print(flex_data);
  // Send data in a format where Max for Live (the plugin which controls the music) can read it
  Serial.print(" ");
  Serial.println(cm);
  delay(50);
}

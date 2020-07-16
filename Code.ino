int red=2;
int green=4;
int orange=3;
int pred=9;
int pgreen=10;
int val=0;
int trig=0;
long cm=0 ,inches=0 ;
void seq();
long microsecondsToInches(long);
long microsecondsToCentimeters(long);
const int pingPin = 7; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 6; // Echo Pin of Ultrasonic Sensor
void buzz();
void setup() {
   Serial.begin(9600); // Starting Serial Terminal
pinMode(red, OUTPUT);
pinMode(green, OUTPUT);
pinMode(orange, OUTPUT);
pinMode(trig, INPUT);
pinMode(8,OUTPUT);
pinMode(9,OUTPUT);
pinMode(10,OUTPUT);
}

void loop() {
  pinMode(green, HIGH);
   long duration, inches, cm;
   pinMode(pingPin, OUTPUT);
   digitalWrite(pingPin, LOW);
   delayMicroseconds(2);
   digitalWrite(pingPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin, LOW);
   pinMode(echoPin, INPUT);
   duration = pulseIn(echoPin, HIGH);
   inches = microsecondsToInches(duration);
   cm = microsecondsToCentimeters(duration);
   Serial.print(inches);
   Serial.print("in, ");
   Serial.print(cm);
   Serial.print("cm");
   Serial.println();
   delay(100);

if(cm<10)
{
  seq();
  }
else{
digitalWrite(green,HIGH);
digitalWrite(pred,HIGH);
}
}
void seq()
{
  digitalWrite(green, LOW);
  delay(1000);
  digitalWrite(orange,HIGH);
  digitalWrite(pred,LOW);
  delay(1000);
  digitalWrite(orange,LOW);
  digitalWrite(red,HIGH);
  digitalWrite(pgreen,HIGH);
  delay(25000);
  buzz();
  
  digitalWrite(red,LOW);
  digitalWrite(pgreen,LOW);
  delay(1000);
  digitalWrite(pred,HIGH);
  digitalWrite(orange,HIGH);
  delay(1000);
  digitalWrite(orange,LOW);
  delay(1000);
  digitalWrite(green, HIGH);
  delay(180000);

}
long microsecondsToInches(long microseconds) {
   return microseconds / 74 / 2;
}

long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}
void buzz()
{
  digitalWrite(8,HIGH);
  delay(5000);
  digitalWrite(8,LOW);
}



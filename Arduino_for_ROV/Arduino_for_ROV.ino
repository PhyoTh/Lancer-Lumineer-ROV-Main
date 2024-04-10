#include <ArduinoJson.h> //Load Json Library
#include<Servo.h>

boolean DEBUG = false;

// SERVO DEFINITIONS and ASSIGN SIGNALS
Servo servo_lf;
byte servoPin_lf= 22; //clockwise; horizontal

Servo servo_rt;
byte servoPin_rt= 23; //counter-clockwise; horizontal

Servo servo_up2;
byte servoPin_up2 = 24; //clockwise; vertical

Servo servo_up1;
byte servoPin_up1 = 25; //counter-clockwise; vertical

Servo servo_claw; 
byte servoPin_claw = 26; //assigning pin 26 to main claw

Servo servo_rotate;
byte servoPin_rotate = 27; //assigning pin 27 to servo 1

// SETUP
int val; //variable for temperature reading
int tempPin = A1; //define analog pin to read
void setup() 
{
  pinMode(LED_BUILTIN, OUTPUT); //initialize digital pin LED_BUILTIN as an output.
  pinMode(44,OUTPUT);
  digitalWrite(13,LOW);
  
  // Attach servo to each belonging signal
  servo_lf.attach(servoPin_lf);
  servo_rt.attach(servoPin_rt);
  servo_up2.attach(servoPin_up2);
  servo_up1.attach(servoPin_up1);
  servo_claw.attach(servoPin_claw);
  servo_rotate.attach(servoPin_rotate);
  delay(7000); //delay to allow ESC to recognize the stopped signal
}

// MAIN
void loop()
{
  Serial.begin(9600); //need to be reopened because of Serial.end() at the end
  while (!Serial.available()) { //exception if it can't read the BYTES sent from the serial port
    digitalWrite(13,HIGH);
    delay(100);
    digitalWrite(13,LOW);
    delay(100); }

  //String thruster = Serial.readStringUntil( '\x7D' ); //read characters/date from serial port until "}" and buffer it into a string
  String get_data = Serial.readStringUntil('\n');
  Serial.setTimeout(10); //set maximum 10ms to wait for serial data (not necessary)

  StaticJsonDocument<2000> json_doc; //create StaticJsonDocument to read
  DeserializationError error = deserializeJson(json_doc,get_data); //deserialize/decode the BYTES read from serial in json format
  if (error){
    Serial.print("Parsing failed: ");
    Serial.println(error.c_str());
    return;
  }
  // After parsing BYTES from serial
  if (DEBUG)
  {
    Serial.println("Received JSON: " + get_data); //print to serial monitor (9600)
    Serial.println();
    // delay(1000);
  }
  
  // Left Thruster
  float th_left = json_doc["tleft"];
  int th_left_sig = (th_left + 1) * 400 + 1100; //map controller
  servo_lf.writeMicroseconds(th_left_sig); //send signal back to servo

  // Right Thruster
  float th_right = json_doc["tright"];
  int th_right_sig = (th_right + 1) * 400 + 1100;
  servo_rt.writeMicroseconds(th_right_sig);

  // Vertical Thurster 1
  float th_up_1 = json_doc["tup"];
  int th_up_sig_1 = (th_up_1 + 1) * 400 + 1100;
  servo_up1.writeMicroseconds(th_up_sig_1);

  // Vertical Thurster 2 *need to get to individual tupL and tupR datas from Python
  float th_up_2 = json_doc["tup"];
  int th_up_sig_2 = (th_up_2 + 1) * 400 + 1100;
  servo_up2.writeMicroseconds(th_up_sig_2);

  // Main Claw Servo
  int clawInput = json_doc["claw"]; // inputs range from 0 to 100
  int clawSignal = clawInput * 10 + 900; // range from 900 to 1700
  servo_claw.writeMicroseconds(clawSignal);

  // Claw Rotate Servo
  int rotateInput = json_doc["claw_rotate"]; // inputs range from 0 to 100
  int rotateSignal = rotateInput * 10 + 900; // range from 900 to 1700
  servo_rotate.writeMicroseconds(rotateSignal);

  // Read Temp
  val = analogRead(tempPin); //read arduino pin
  float mv = ((val/1024.0)*500);
  float cel = (mv/10); //temperature in Celsius

  // Write and send those values back in Json format
  StaticJsonDocument<2000> doc;//define StaticJsonDocument

  //doc["temp"] = cel; *Python doesn't even read this??? 
  doc["volt"] = mv;
  doc["temp"] = cel;
  doc["tleft"] = th_left_sig;
  doc["tright"] = th_right_sig;
  doc["tupL"] = th_up_sig_1;
  doc["tupR"] = th_up_sig_2;
  doc["claw"] = clawSignal;
  doc["claw_rotate"] = rotateSignal;

  serializeJson(doc,Serial); //convert to Json string,sends to surface
  Serial.end(); //to allow Python to use it
  delay(50); //allow gap time for Python
}
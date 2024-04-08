#include <ArduinoJson.h> //Load Json Library
#include<Servo.h>

// SERVO DEFINITIONS
Servo servo_lf;
Servo servo_rt;
Servo servo_up1;
Servo servo_up2;
Servo servo_claw; 
Servo servo_rotate;

// ASSIGN SIGNALS
int val; //variable for temperature reading
int tempPin = A1;//define analog pin to read
byte servoPin_rt= 23; //counter-clockwise; horizontal
byte servoPin_lf= 22; //clockwise; horizontal
byte servoPin_up1 = 25; //counter-clockwise; vertical
byte servoPin_up2 = 24; //clockwise; vertical
byte servoPin_claw = 26; //Assigning pin 26 to main claw
byte servoPin_rotate = 27; //Asigning pin 27 to servo 1

void setup() 
{
  pinMode(LED_BUILTIN, OUTPUT);// initialize digital pin LED_BUILTIN as an output.
  pinMode(44,OUTPUT);
  digitalWrite(13,LOW);
  Serial.begin(9600);
  servo_up1.attach(servoPin_up1);
  servo_up2.attach(servoPin_up2);
  servo_lf.attach(servoPin_lf);
  servo_rt.attach(servoPin_rt);
  servo_claw.attach(servoPin_claw); // Creating servo object for main claw
  servo_rotate.attach(servoPin_rotate);
  
  delay(7000); //delay to allow ESC to recognize the stopped signal
}

void loop() 
{
  String thruster;
    
  while (!Serial.available())
  { 
   //Serial.print("No data");
   digitalWrite(13,HIGH);
   delay(100);
   digitalWrite(13,LOW);
   delay(100);
  }
  if(Serial.available()) 
  {
    thruster=Serial.readStringUntil( '\x7D' );//Read data from Arduino until "}";
    Serial.println("Received JSON: " + thruster); // Debugging statement
  
    StaticJsonDocument<5000> json_doc; //the StaticJsonDocument we write to
    deserializeJson(json_doc,thruster);
     
    //Left Thruster
    float th_left=json_doc["tleft"];
    int th_left_sig=(th_left+1)*400+1100; //map controller to servo
    servo_lf.writeMicroseconds(th_left_sig); //Send signal to ESC
    
    //Right Thruster
    float th_right=json_doc["tright"];
    int th_right_sig=(th_right+1)*400+1100; //map controller to servo
    servo_rt.writeMicroseconds(th_right_sig); //Send signal to ESC
   
    //Vertical Thruster 1 
    float th_up_1 = json_doc["tup"];
    int th_up_sig_1=(th_up_1+1)*400+1100; //map controller to servo
    servo_up1.writeMicroseconds(th_up_sig_1); //Send signal to ESC

    //Vertical Thruster 2
    float th_up_2 = json_doc["tup"];
    int th_up_sig_2=(th_up_2+1)*400+1100; //map controller to servo
    servo_up2.writeMicroseconds(th_up_sig_2); //Send signal to ESC
    
    // Main Claw Code
    int clawInput = json_doc["claw"]; // inputs range from 0 to 100
    int clawSignal = clawInput*10+900; // range from 900 to 1700
    servo_claw.writeMicroseconds(clawSignal); // Send the signal back to Python

    // Rotating Claw Code
    int rotateInput = json_doc["rotate"]; // inputs range from 0 to 100
    int rotateSignal = rotateInput*10+900; // range from 900 to 1700
    servo_rotate.writeMicroseconds(rotateSignal); // Send the signal back to Python

//Read Temperature, return to surface
    val=analogRead(tempPin);//read arduino pin
    StaticJsonDocument<500> doc;//define StaticJsonDocument
    float mv = ((val/1024.0)*500);
    float cel = (mv/10);//temperature in Celsius
    doc["temp"]=cel;//add temp to StaticJsonDocument
    doc["volt"]=mv;
    doc["sig_up_1"]=th_up_sig_1;
    doc["sig_up_2"]=th_up_sig_2;
    doc["sig_rt"]=th_right_sig;
    doc["sig_lf"]=th_left_sig;
    doc["claw"]=clawSignal;
    doc["rotate"]=rotateSignal;
    
    serializeJson(doc,Serial);//convert to Json string,sends to surface
    Serial.println();//newline
    delay(10);
  }
}
# PyDuino
PyQt App for Arduino

## App Demo
![demo](http://i.imgur.com/dlLJiw8.gif)

## Arduino Code

```arduino
#define led 13
#define baud 9600

void setup() {
  pinMode(led, OUTPUT);
  Serial.begin(baud);
}

void loop() { }
void serialEvent(){
  if (Serial.available() > 0){
    //
    String command = Serial.readStringUntil('\n');
    
    //Sending a reply after executing the function
    if (command.equals("on")) { digitalWrite(led, HIGH); Serial.println("LED ON"); }
    else if (command.equals("off")) { digitalWrite(led, LOW); Serial.println("LED OFF"); }
  }
}
```

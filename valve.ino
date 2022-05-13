int input_data;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13,LOW);
}

void loop() {
  while(Serial.available())
  {
    input_data = Serial.read();
  }

  if(input_data == '1')
  {
    digitalWrite(13, HIGH); // valve_open
  }
  else if(input_data == '0')
  {
    digitalWrite(13, LOW); // valve_close
  }
}


int analog_entry[6];
int value;
int good_values[6] = {0,203,409,614,820,1023};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  for(int i=0;i<6;i++){
    analog_entry[i]=analogRead(i);
  }
  Serial.println(create_message(analog_entry));
}


int check_value(int to_check){
  for(int i=0;i<6;i++){
    if(to_check==good_values[i] || to_check-1==good_values[i] || to_check+1==good_values[i]){
      return i;
      Serial.println("Returned i !");
    }
  }
  return 6;
}

String create_message(int data[]) {
  String msg=String(check_value(data[0]))+String(check_value(data[1]))+String(check_value(data[2]))+String(check_value(data[3]))+String(check_value(data[4]))+String(check_value(data[5]));
  return msg;
}
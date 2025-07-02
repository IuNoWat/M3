
#include "RunningAverage.h"

RunningAverage entry_0(5);
RunningAverage entry_1(5);
RunningAverage entry_2(5);
RunningAverage entry_3(5);
RunningAverage entry_4(5);
RunningAverage entry_5(5);
int value;
int good_values[6] = {0,203,409,614,820,1023};
float var;
float avg;
String msg;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  
  entry_0.addValue(analogRead(0));
  entry_1.addValue(analogRead(1));
  entry_2.addValue(analogRead(2));
  entry_3.addValue(analogRead(3));
  entry_4.addValue(analogRead(4));
  entry_5.addValue(analogRead(5));

  msg="";

  if(entry_0.getCoefficientOfVariation()<0.1 || isnan(entry_0.getCoefficientOfVariation())){
    avg=entry_0.getAverage();
    msg=msg+check_avg(avg);
  } else {
    msg=msg+"6";
  }

  if(entry_1.getCoefficientOfVariation()<0.1 || isnan(entry_1.getCoefficientOfVariation())){
    avg=entry_1.getAverage();
    msg=msg+check_avg(avg);
  } else {
    msg=msg+"6";
  }

  if(entry_2.getCoefficientOfVariation()<0.1 || isnan(entry_2.getCoefficientOfVariation())){
    avg=entry_2.getAverage();
    msg=msg+check_avg(avg);
  } else {
    msg=msg+"6";
  }

  if(entry_3.getCoefficientOfVariation()<0.1 || isnan(entry_3.getCoefficientOfVariation())){
    avg=entry_3.getAverage();
    msg=msg+check_avg(avg);
  } else {
    msg=msg+"6";
  }

  if(entry_4.getCoefficientOfVariation()<0.1 || isnan(entry_4.getCoefficientOfVariation())){
    avg=entry_4.getAverage();
    msg=msg+check_avg(avg);
  } else {
    msg=msg+"6";
  }

  if(entry_5.getCoefficientOfVariation()<0.1 || isnan(entry_5.getCoefficientOfVariation())){
    avg=entry_5.getAverage();
    msg=msg+check_avg(avg);
  } else {
    msg=msg+"6";
  }

  Serial.println(msg);
}

String check_avg(float to_check) {
  if(to_check<0.05){
    return "0";
  }
  for(int i=1;i<6;i++){
    if(good_values[i]+2>to_check && to_check>good_values[i]-2){
      return String(i);
    }
  }
  return "6";
}



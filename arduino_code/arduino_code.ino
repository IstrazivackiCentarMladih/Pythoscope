// Write string content on the microcontroller outputs
void writeOscilloscope (char* string){
  //Channel 1
  digitalWrite(2, string[1]>>1 & 1);
  digitalWrite(3, string[1]>>2 & 1);
  digitalWrite(4, string[1]>>3 & 1);
  digitalWrite(5, string[1]>>4 & 1);
  digitalWrite(6, string[1]>>5 & 1);
  digitalWrite(7, string[1]>>6 & 1);
  digitalWrite(8, string[1]>>7 & 1);

  //Channel 2
  digitalWrite(A5, string[2]>>1 & 1);
  digitalWrite(A4, string[2]>>2 & 1);
  digitalWrite(13, string[2]>>3 & 1);
  digitalWrite(12, string[2]>>4 & 1);
  digitalWrite(11, string[2]>>5 & 1);
  digitalWrite(10, string[2]>>6 & 1);
  digitalWrite( 9, string[2]>>7 & 1);
  }

void setup() {
  
  // Channel 1

  pinMode (2, OUTPUT);
  pinMode (3, OUTPUT);
  pinMode (4, OUTPUT);
  pinMode (5, OUTPUT);
  pinMode (6, OUTPUT);
  pinMode (7, OUTPUT);
  pinMode (8, OUTPUT);

  //Channel 2  
  pinMode (9, OUTPUT);
  pinMode (10, OUTPUT);
  pinMode (11, OUTPUT);
  pinMode (12, OUTPUT);
  pinMode (13, OUTPUT);
  pinMode (A4, OUTPUT);
  pinMode (A5, OUTPUT);
  
  Serial.begin(115200);
}
  char inputString[5];
  char correct_input;
  bool new_input;
  unsigned long correct=0;
  unsigned long wrong=0;

void loop() 
{
    if(Serial.available()>0) {
      //Check for the synchronization byte
      if(Serial.peek()!='S') 
        while(Serial.peek()!='S') Serial.read();
      Serial.readBytes(inputString, 5);
        if (inputString[0]=='S' & inputString[3]=='\r' & inputString[4]=='\n'){
          new_input=true;
          correct++;
          //Serial.print(inputString);
          }
        else{
          //Serial.print("Wrong input:"); 
          //Serial.println(inputString);
          wrong++;
          }
      }
      
      //Serial.print("Wrong: "); Serial.print(wrong); Serial.print(", correct: "); Serial.println(correct);
      if (new_input){
        writeOscilloscope(inputString);
        //Serial.println("ok");
        new_input=false;
        }  
}




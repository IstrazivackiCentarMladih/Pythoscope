
unsigned char channel1[500]={70,70,70,70,70,70,60,60,60,60,60,60,60,60,60,60,60,60,70,70,70,70,70,70,75,79,83,87,92,96,101,107,114,123,123,115,108,104,101,97,94,91,88,85,85,87,90,94,99,102,107,111,118,124,125,127,128,128,128,127,127,127,127,128,128,128,128,132,138,143,146,150,155,158,161,165,169,173,176,179,182,186,190,196,196,196,197,197,197,197,197,197,197,197,197,196,190,189,190,190,190,190,190,190,190,189,190,183,180,176,173,167,161,154,152,150,146,143,141,140,140,140,140,141,140,141,140,140,140,140,133,126,116,108,102,98,93,87,82,77,73};
unsigned char channel2[500]={34,38,42,46,50,54,54,50,46,42,38,34,30,26,22,18,14,10,10,14,18,21,26,30,33,37,40,43,46,49,51,53,54,55,52,51,49,47,45,43,40,38,35,32,29,27,24,22,19,16,14,12,11,12,9,14,17,21,25,29,32,36,40,43,47,51,55,55,55,52,49,46,43,40,38,37,39,42,45,48,51,54,55,55,50,46,43,38,34,29,26,22,19,16,12,9,8,12,16,20,24,28,32,36,40,44,48,44,39,36,34,34,33,33,36,39,41,44,46,47,42,38,34,30,27,23,18,15,11,8,8,8,8,9,10,13,16,18,21,24,28};


int dot_number=141;


void oscilloscopeWrite(int ch1, int ch2){
      digitalWrite(0, ch1    & 0b00000001);
      digitalWrite(1, ch1>>1 & 0b00000001);
      digitalWrite(2, ch1>>2 & 0b00000001);
      digitalWrite(3, ch1>>3 & 0b00000001);
      digitalWrite(4, ch1>>4 & 0b00000001);
      digitalWrite(5, ch1>>5 & 0b00000001);
      digitalWrite(6, ch1>>6 & 0b00000001);
      digitalWrite(7, ch1>>7 & 0b00000001);
  
      digitalWrite(A0, ch2>>1 & 0b00000001);
      digitalWrite(13, ch2>>2 & 0b00000001);
      digitalWrite(12, ch2>>3 & 0b00000001);
      digitalWrite(11, ch2>>4 & 0b00000001);
      digitalWrite(10, ch2>>5 & 0b00000001);
      digitalWrite(9,  ch2>>6 & 0b00000001);
      digitalWrite(8,  ch2>>7 & 0b00000001);
        
  }

void readNew(){
  char input;
  bool flag_start, flag_ch1, flag_ch2, flag_end, flag_length;
  flag_start=false;
  flag_ch1=false;
  flag_ch2=false;
  flag_end=false;
  flag_length=false;

  while(Serial.available()>0 & !flag_end){
    input=Serial.read();
    switch (input){
      case 'S': 
        flag_start=true;
        flag_ch1=false;
        flag_ch2=false;
        flag_end=false;
        flag_length=false;
        break;
      case 'L':  
      
      }
    
    }
    
  }


void setup() {
  
  // Channel 1
  pinMode (0, OUTPUT);
  pinMode (1, OUTPUT);
  pinMode (2, OUTPUT);
  pinMode (3, OUTPUT);
  pinMode (4, OUTPUT);
  pinMode (5, OUTPUT);
  pinMode (6, OUTPUT);
  pinMode (7, OUTPUT);

  //Channel 2  
  pinMode (8, OUTPUT);
  pinMode (9, OUTPUT);
  pinMode (10, OUTPUT);
  pinMode (11, OUTPUT);
  pinMode (12, OUTPUT);
  pinMode (13, OUTPUT);
  pinMode (A0, OUTPUT);

  Serial.begin(115200);
}
void loop() 
{
    if(Serial.available()>0)
      readNew();  
    int i;

          
    for (i=0; i<dot_number;i++){
      oscilloscopeWrite(channel1[i],channel2[i]);
    
      }
}




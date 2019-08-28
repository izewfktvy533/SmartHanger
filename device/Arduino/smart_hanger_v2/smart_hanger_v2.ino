#include "XBee.h"
#include "DHT.h"

#define DHT_TYPE DHT22
#define CENTER_DHT 8
#define LEFT_DHT   3
#define RIGHT_DHT  4


const int BITRATE = 9600;
DHT center_sensor(CENTER_DHT, DHT_TYPE);
DHT left_sensor(LEFT_DHT, DHT_TYPE);
DHT right_sensor(RIGHT_DHT, DHT_TYPE);

XBee xbee = XBee();
XBeeAddress64 addr64;
ZBRxResponse  rxResponse;
ZBTxRequest   txRequest;



inline void convertFloatToChar(char* str, float value)
{
    int whl;
    unsigned int frac;
    boolean inverse = false; //符号
 
    whl = (int)value;                //整数
    frac = (unsigned int)(value * 100) % 100; //少数
 
    if(whl < 0){
        whl *= -1;
        inverse = true;
    }
 
    if(inverse == true){
        sprintf(str, "-%d.%02d", whl, frac);
    }
    else{
        sprintf(str, "%d.%02d", whl, frac);
    }

}



/*
inline bool canGetResponse(uint8_t api_id) {
  if (xbee.getResponse().isAvailablie()) {
    if (xbee.getResponse().getApiId() == api_id) return true;
    else return false;
  }
  else return false;
}
*/



inline bool canGetResponse(uint8_t api_id) {
  if (xbee.getResponse().getApiId() == api_id) return true;
  else return false;
}



inline bool canReadRxResponse(uint32_t timeout, uint8_t api_id) {
  bool can_read_packet_bool = true;
  
  if(timeout == 0) {
    xbee.readPacket();
  }
  else if(timeout > 0) {
    can_read_packet_bool = xbee.readPacket(timeout);
  }
  else return false;

  if (can_read_packet_bool && canGetResponse(api_id)) {
    xbee.getResponse().getZBRxResponse(rxResponse);
    return true;
  }
  else return false;

}



inline String getRecievedData() {
    return (String)((char*)(rxResponse.getFrameData() + 11));
}



inline void startHandShake() {
  // ブロードキャストを受信
  while(true) {
    while(!canReadRxResponse(0, ZB_RX_RESPONSE));
    if(rxResponse.getFrameData()[10] == 2 && getRecievedData().compareTo("start")) break; 
  }

  // ゲートウェイ側のアドレスを取得
  addr64 = rxResponse.getRemoteAddress64();
}



inline bool isFinishHandShake() {
  // ブロードキャストを受信
  while(!canReadRxResponse(0, ZB_RX_RESPONSE));
  if(rxResponse.getFrameData()[10] == 2 && getRecievedData().compareTo("finish")) true; 
  else false;
}



void reset() {
  asm volatile ("  jmp 0");  
} 



void setup() {
  pinMode(CENTER_DHT, INPUT);
  pinMode(LEFT_DHT, INPUT);
  pinMode(RIGHT_DHT, INPUT);
  Serial.begin(BITRATE);
  xbee.setSerial(Serial);
  startHandShake();
}



void loop(){
  int start_time_m = millis();

  //if(isFinishHandShake()) reset();
  
  float center_tem = center_sensor.readTemperature();
  float center_hum = center_sensor.readHumidity();
  float left_tem = left_sensor.readTemperature();
  float left_hum = left_sensor.readHumidity();
  float right_tem = right_sensor.readTemperature();
  float right_hum = right_sensor.readHumidity();


  char data_json[256];
  char center_tem_str[16];
  char center_hum_str[16];
  char left_tem_str[16];
  char left_hum_str[16];
  char right_tem_str[16];
  char right_hum_str[16];

  memset(data_json, 0, 256);
  memset(center_tem_str, 0, 16);
  memset(center_hum_str, 0, 16);
  memset(left_tem_str, 0, 16);
  memset(left_hum_str, 0, 16);
  memset(right_tem_str, 0, 16);
  memset(right_hum_str, 0, 16);

  convertFloatToChar(center_tem_str, center_tem);
  convertFloatToChar(center_hum_str, center_hum);
  convertFloatToChar(left_tem_str,   left_tem);
  convertFloatToChar(left_hum_str,   left_hum);
  convertFloatToChar(right_tem_str,  right_tem);
  convertFloatToChar(right_hum_str,  right_hum);

  sprintf(data_json, "{'center_tem':%s, 'center_hum':%s, 'left_tem':%s, 'left_hum':%s, 'right_tem':%s, 'right_hum':%s}", center_tem_str, center_hum_str, left_tem_str, left_hum_str, right_tem_str, right_hum_str);
  

  ZBTxRequest zbTx = ZBTxRequest(addr64, data_json, strlen(data_json));
  xbee.send(zbTx);

  /*** mesuring run time ***/
  int finish_time_m = millis();
  /*
  Serial.print(finish_time_m - start_time_m);
  Serial.print(" + ");
  */
  int delta = finish_time_m - start_time_m;

  if (delta < 3000) {
    delay(3000 - delta);
  }

}

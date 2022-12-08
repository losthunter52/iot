#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>

#ifndef STASSID
#define STASSID "ADS_IOT"
#define STAPSK  "adsifsc2022"
#endif

#define DHTTYPE DHT11
#define dht_dpin 0

const char *ssid = STASSID;
const char *password = STAPSK;

StaticJsonDocument<200> json;

String serverName = "http://192.168.1.79:1880/update-esp8266";

String returnJson() {
  char temp[400]; 
  int l = random(0,99);
  Serial.print("Luminosidade = ");
  Serial.println(l);
  Serial.println(" ");
  
  
  json["luminosidade"] = l;
  
  serializeJsonPretty(json, temp);
  
  return temp;
}

void setup(void) {
  Serial.begin(9600);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println(" ");
  
}

void loop(void) {
  delay(2000);
  if(WiFi.status()== WL_CONNECTED){
    WiFiClient client;
    HTTPClient http;  
    // Your Domain name with URL path or IP address with path
    http.begin(client, serverName);

    http.addHeader("Content-Type", "application/json");

    String json = returnJson();
    Serial.print(json);
    Serial.println(" ");
    int httpResponseCode = http.POST(json);

    Serial.println(" ");
    Serial.print("HTTP Response code: ");
    Serial.print(httpResponseCode);
    Serial.println(" ");
    Serial.println(" ");
    http.end();
  }
}
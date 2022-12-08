#include <SPI.h>
#include <Ethernet.h>
#include <ArduinoJson.h>

byte mac[] = {0x90, 0xA2, 0xDA, 0x0D, 0xF6, 0xFF};
IPAddress server(192, 168, 1, 79);

EthernetClient client;

StaticJsonDocument<200> json;

String returnJson() {
  char temp[400];
  int t = random(12, 32);
  int u = random(50, 99);
  Serial.print("Temperatura = ");
  Serial.println(t);
  Serial.print("Umidade = ");
  Serial.println(u);
  Serial.println(" ");

  json["temperatura"] = t;
  json["umidade"] = u;

  serializeJsonPretty(json, temp);

  return temp;
}

void setup() {
  Ethernet.begin(mac);
  Serial.begin(9600);
  Serial.println(Ethernet.localIP());
  delay(1000);
  delay(1000);
  Serial.println("connecting...");
}

void post_json() {
  String json = returnJson();

  if (client.connect(server, 1880)) {
    Serial.println("Sending to Server: ");
    client.println("POST /update-arduino HTTP/1.1");
    client.println("User-Agent: arduino/1.0");
    client.println("Accept-Encoding: gzip, deflate");
    client.println("Accept: */*");
    client.println("Connection: keep-alive");
    client.print("Content-Length: ");
    client.println(json.length());
    client.println("Content-Type: application/json");
    client.println();
    client.print(json);
    client.println();
    client.println();
  }
  else {
    Serial.println("Cannot connect to Server");
  }
  delay(1000);
}

void loop() {

  post_json();

  if (client.available()) {
    char c = client.read();
    Serial.println(c);
  }

  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnected");
    client.stop();
  }
}
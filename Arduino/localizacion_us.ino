//Incluir las librerías necesarias para ejecutar el codigo

#include <Pozyx.h>                    //Comunicación con la baliza Poxyz
#include <Pozyx_definitions.h>        //Librería de la Poxyz
#include <Wire.h>                     //Uso de librerías
#include "Adafruit_HTU21DF.h"         //Librería del sensor de Temperatura y humedad
#include "Adafruit_SGP30.h"           //Librería del sensor de Calidad de aire


//Se incluyen los sensores de temperatura y calidad de aire
Adafruit_HTU21DF htu = Adafruit_HTU21DF(); 
//objeto creado para el sensor de humedad y temperatura
Adafruit_SGP30 sgp; 
//objeto creado para el sensor de calidad de aire

//Parámetros del sensor de ultrasonidos
unsigned char txbuf[10] = {0}; //buffer de trasmision
unsigned char rxbuf[10] = {0}; //bufer de recepcion


typedef enum { //enumeracion de indices para acceder a los registros de comunicacion ¿del ultrasonidos?

  SLAVEADDR_INDEX = 0,
  PID_INDEX,
  VERSION_INDEX ,

  DIST_H_INDEX,
  DIST_L_INDEX,

  TEMP_H_INDEX,
  TEMP_L_INDEX,

  CFG_INDEX,
  CMD_INDEX,
  REG_NUM

} regindexTypedef;

#define    MEASURE_MODE_PASSIVE    (0x00) //Medicion pasiva en sensor Pozyx
#define    MEASURE_RANG_500        (0x20) //rango de medicion 5m del sensor Pozyx
#define    CMD_DISTANCE_MEASURE    (0x01) //Constante para iniciar la medicion, al enviar este comando se inicia la medida 

unsigned char addr0 = 0x11;
unsigned char addr1 = 0x12;
unsigned char addr2 = 0x13;
unsigned char addr3 = 0x15;
unsigned char addr4 = 0x14;

int16_t distances[5];

String cad;   //Se crea un string que recogerá los datos de los sensores para la Rapsberry

//Envia o recibe 32 bytes por el puerto serie para el sensor de temperatura y humedad
uint32_t getAbsoluteHumidity(float temperature, float humidity) {
    // Aproximación de la fórmula de Sensirion SGP30 Driver Integration chapter 3.15
    const float absoluteHumidity = 216.7f * ((humidity / 100.0f) * 6.112f * exp((17.62f * temperature) / (243.12f + temperature)) / (273.15f + temperature)); // [g/m^3]
    const uint32_t absoluteHumidityScaled = static_cast<uint32_t>(1000.0f * absoluteHumidity); // [mg/m^3]
    return absoluteHumidityScaled;
}
uint16_t remote_id = 0x6000;                  // Lectura del ID de las balizas
bool remote = false;                          // Comprobar la conexión remota de la ID de las balizas

boolean use_processing = false;               // Comprobación del proceso de recopilación de datos de las balizas

const uint8_t num_anchors = 4;                                       // Número de balizas
uint16_t anchors[num_anchors] = {0x6e44, 0x6e71, 0x6e7d, 0x6932};    // Código en orden de las balizas
int32_t anchors_x[num_anchors] = {0, 1300, 400, 350};             // Posición X de las balizasa en mm
int32_t anchors_y[num_anchors] = {0, 0, 795, 795};                 // Posicion Y de las balizas en mm
int32_t heights[num_anchors] = {565, 735, 495, 300};             // Posicion Z de las balizas en mm (altura)

uint8_t algorithm = POZYX_POS_ALG_UWB_ONLY;             // Algoritmo de uso. try POZYX_POS_ALG_TRACKING para un rápido movimiento respecto a los objetos.
uint8_t dimension = POZYX_3D;                           // Posicionamiendo de las dimensiones segun la posicion en 3D
int32_t height = 220;                                   // Altura de la baliza maestra aproximada, en mm

//Función de inicio para inicializar variables
void setup(){
   Wire.begin(); // join i2c bus (address optional for master)
   Serial.begin(115200);//9600       //Iniciamos el puerto serie a 115200 Baudios
   while (!Serial) { delay(10); } // Esperamos unos segundos a que la consola se abra  
   // Configurar los modos de medición de los sensores
  configureSensor(addr0);
  configureSensor(addr1);
  configureSensor(addr2);
  configureSensor(addr3);
  configureSensor(addr4);
  
// Incluimos un bucle de error conjunto para saber si hay problemas con los sensores o las balizas
if(Pozyx.begin() == POZYX_FAILURE||!htu.begin()||! sgp.begin()){
  Serial.println("Error en alguno de los sensores o balizas");
  delay(100);
  abort();
}
//Bucle para ejecutar funciones de las balizas en función del comportamiento requerido
if(!remote){
    remote_id = NULL;
  }
  // Limpia los antiguos valores de las blaizas
  Pozyx.clearDevices(remote_id);
  // Posicionamiendo de las balizas en modo manual
  setAnchorsManual();
  // Posicionamiento del algoritmo
  Pozyx.setPositionAlgorithm(algorithm, dimension, remote_id);
  //Llama a la funcion que escribe las coordenadas de las balizas
  printCalibrationResult();
  delay(1000); //Se espera 2 segundos   
}

void configureSensor(unsigned char addr) {
  txbuf[0] = (MEASURE_MODE_PASSIVE | MEASURE_RANG_500);
  i2cWriteBytes(addr, CFG_INDEX, &txbuf[0], 1);
}


void i2cWriteBytes(unsigned char addr_t, unsigned char Reg, unsigned char *pdata, unsigned char datalen) {
  Wire.beginTransmission(addr_t);
  Wire.write(Reg);
  for (uint8_t i = 0; i < datalen; i++) {
    Wire.write(*pdata);
    pdata++;
  }
  Wire.endTransmission();
}

void i2cReadBytes(unsigned char addr_t, unsigned char Reg, unsigned char Num) {
  unsigned char i = 0;
  Wire.beginTransmission(addr_t);
  Wire.write(Reg);
  Wire.endTransmission();
  Wire.requestFrom(addr_t, Num);
  while (Wire.available()) {
    rxbuf[i] = Wire.read();
    i++;
  }
}

void readDistanceSingular(unsigned char addr, int sensorIndex) { #Función de lectira de datos de un sensor ultra sonidos
  int16_t dist;
  
  txbuf[0] = CMD_DISTANCE_MEASURE;
  i2cWriteBytes(addr, CMD_INDEX, &txbuf[0], 1);
  delay(200);
  
  i2cReadBytes(addr, DIST_H_INDEX, 2);
  dist = ((uint16_t)rxbuf[0] << 8) + rxbuf[1];
  
  distances[sensorIndex] = dist; // Almacenar la distancia en el array
}

void readDistances() { #Funcion para leer las distancias de todos los sensores ultrasonidos
  readDistanceSingular(addr0, 0);
  readDistanceSingular(addr1, 1);
  readDistanceSingular(addr2, 2);
  readDistanceSingular(addr3, 3);
  readDistanceSingular(addr4, 4);
}

void printDistances() { #Funcion para imprimir las distancias por el monitor
  for (int i = 0; i < 5; i++) {
    Serial.print("Sensor ");
    Serial.print(i+1);
    Serial.print(": Distance = ");
    Serial.print(distances[i]);
    Serial.print(" cm");
    Serial.println();
  }
}

unsigned char i = 0, x = 0;

//Bucle de repetición donde se leen los sensores
void loop(){
coordinates_t position;   
  int status;
 
  readDistances();
  //printDistances();
  
  delay(100);
 // Bucle que recoge los valores en funcion del tipo de posicionamiento que hayamos hecho
  if(remote){
    status = Pozyx.doRemotePositioning(remote_id, &position, dimension, height, algorithm);
  }else{
    status = Pozyx.doPositioning(&position, dimension, height, algorithm);
  }
 if (status == POZYX_SUCCESS){ //Bucle para ver que si todo el proceso es correcto ejecuta una orden
    // Saca por pantalla el resultado
    printCoordinates(position);
  }
  
}
//Función para leer y sacar por pantalla los valores de los sensores
void printCoordinates(coordinates_t coor){    //Llama a la función de escribir las coordenadas
  uint16_t network_id = remote_id;
  if (network_id == NULL){
    network_id = 0;
  }
  if(!use_processing){ //Si todo el proceso es correcto se ejecuta lo de dentro del bucle
    
    float temp = htu.readTemperature();   //Guardamos en la variable temeratura el valor 
    float rel_hum = htu.readHumidity();   //Guardamos en la variable humedad el valor
    
  //Bucle necesario para recibir los valores de volatiles y CO2
  if (! sgp.IAQmeasure()) {
    return;
  }
  //Bucle necesario para recibir los valores de Crudo de H2 y Ethanol
  if (! sgp.IAQmeasureRaw()) {
    return;
  }

    //Rellenamos la variable que guardará los datos de los sensores y será leída en Python  
    //cad = "#1:" + String(coor.x)+ "#2:" + String(coor.y) +"#3:" + String(coor.z)+"#4:" + String(temp)+"#5:" + String(rel_hum)+"#6:" + String(sgp.TVOC)+"#7:" + String(sgp.eCO2)+"#8:" + String(sgp.rawH2)+"#9:" + String(sgp.rawEthanol)+ "#10:" + String(distances[2])+ "@"+"\n";
    //Serial.println(cad); //Sacamos por pantalla la variable
     // Leer las distancias de los sensores de ultrasonidos
    int distance0 = distances[0];
    int distance1 = distances[1];
    int distance2 = distances[2];
    int distance3 = distances[3];
    int distance4 = distances[4];

    // Rellenamos la variable que guardará los datos de los sensores y será leída en Python
    cad = "#1:" + String(coor.x) + "#2:" + String(coor.y) + "#3:" + String(coor.z) +
          "#4:" + String(temp) + "#5:" + String(rel_hum) + "#6:" + String(sgp.TVOC) +
          "#7:" + String(sgp.eCO2) + "#8:" + String(sgp.rawH2) + "#9:" + String(sgp.rawEthanol) +
          "#10:" + String(distance0) + "#11:" + String(distance1) + "#12:" + String(distance2) +
          "#13:" + String(distance3) + "#14:" + String(distance4) + "@" + "\n";

    Serial.println(cad); // Sacamos por pantalla la variable

  }else{
    Serial.print("POS,0x692C");
    Serial.print(network_id,HEX);
    Serial.print(",");
    Serial.print(coor.x);
    Serial.print(",");
    Serial.print(coor.y);
    Serial.print(",");
    Serial.println(coor.z);
  }
  delay(500);
}
//Función individual que escribe los valores de posición de las balizas, puede ser llamado muchas veces para ejecutarse
void printCalibrationResult(){
  uint8_t list_size;
  int status;

  status = Pozyx.getDeviceListSize(&list_size, remote_id);
  uint16_t device_ids[list_size];
  status &= Pozyx.getDeviceIds(device_ids, list_size, remote_id);

  coordinates_t anchor_coor;
  for(int i = 0; i < list_size; i++)
  {
   //Bucle que saca por pantalla las coordenadas. Se elimina porque sino Python crea más variables de las que debe para subir a la BBDD
  }
}

void setAnchorsManual(){    //Función para la colocación de balizas de modo manual, que es la que se va a usar. Puede ser llamada muchas veces
  for(int i = 0; i < num_anchors; i++){
    device_coordinates_t anchor;
    anchor.network_id = anchors[i];
    anchor.flag = 0x1;
    anchor.pos.x = anchors_x[i];
    anchor.pos.y = anchors_y[i];
    anchor.pos.z = heights[i];
    Pozyx.addDevice(anchor, remote_id);
  }

  //En caso de que el numero de balizas seaea mayor que 4, el módo de localización se modifica.NO es nuestro caso pero si es necesrio tenerlo configurado
  if (num_anchors > 4){
    Pozyx.setSelectionOfAnchors(POZYX_ANCHOR_SEL_AUTO, num_anchors, remote_id);
  }
}

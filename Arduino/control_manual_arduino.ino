// Motor A DERECHO
int E1 = 6;
int M1 = 7;

// Motor B IZQUIERDO
int E2 = 5;
int M2 = 4;

//En esta función indicamos la inicializacion de las señales de salida, en este caso, los dos motores. Además inicalizamos el puerto serie para ver lo que obtenemos
//Esto solo se ejecuta una vez
int prueba = 8;
int noentra =9;
void setup ()
{
 // Declaramos todos los pines como salidas
 pinMode (M1, OUTPUT);
 pinMode (M2, OUTPUT);
 pinMode(prueba, OUTPUT);
 pinMode(noentra, OUTPUT);
 Serial.begin(9600);//Inicializamos el puerto serie a los baudios correspondientes
 digitalWrite(prueba, LOW);
 digitalWrite(noentra,LOW);
}
 //Ahora de manera independiente vamos a crear las distintas funciones que moveran el robot en distintos sentidos.
 //Estas funciones permiten una mejor organización en el código ya que cuando queramos usarlas solo tienen que ser llamadas,
 //no hace falta escribir todo lo que hacen cada vez que se usen.



void loop() {
  digitalWrite(prueba,LOW);
  digitalWrite(noentra, LOW);
  
  //Este bucle ejecuta las funciones explicadas más arriba. La raspberry es quien da las ordenes a la placa arduino, quien ejecuta las
  //funciones de movimiento. Para ello tiene que leer lo que se escriba por teclado.
 
   while (!Serial.available())
  {
    ; // Espero
  }
 
  
  String teststr = Serial.readString();  //read until timeout
  //digitalWrite(prueba,LOW);
  char c[50];
  teststr.toCharArray(c, 50);
  Serial.print("Leyendo C:");
  Serial.println(c);
  // remove any \r \n whitespace at the end of the String
  //Serial.println(teststr);
   if (c[0] == 'W') { //Si es una 'W', avanza hacie delante
         Serial.println("Adelante 2");
         digitalWrite(prueba,HIGH);
         //Adelante();
         digitalWrite (M1, LOW);
          analogWrite (E1,150); //Velocidad motor A
            //Direccion motor B
          digitalWrite (M2, HIGH);
          analogWrite (E2,150); //Velocidad motor B
         delay(2000);
      } 
    else if (c[0] == 'S'){ //Atras()
        //Direccion motor A
        digitalWrite (M1, HIGH);
        analogWrite (E1,150); //Velocidad motor A
        //Direccion motor B
        digitalWrite (M2, LOW);
        analogWrite (E2,150); //Velocidad motor B
    }
    else if (c[0] == 'A'){ //Izquierda
        //Direccion motor A
        digitalWrite (M1, LOW);
        analogWrite (E1,220); //Velocidad motor A
          //Direccion motor B
        digitalWrite (M2, LOW);
        analogWrite (E2,220); //Velocidad motor B
     }
    else if (c[0] == 'D'){ //Derecha
      //Direccion motor A
        digitalWrite (M1, HIGH);
        analogWrite (E1,220); //Velocidad motor A
      //Direccion motor B
        digitalWrite (M2, HIGH);
        analogWrite (E2,220); //Velocidad motor B
    }
    else if (c[0] == 'Q'){ //Avanza y gira hacia la izquierda
        //Direccion motor A
        digitalWrite (M1, LOW);
        analogWrite (E1,150); //Velocidad motor A
        //Direccion motor B
        digitalWrite (M2, HIGH);
        analogWrite (E2,100); //Velocidad motor B
    }
    else if (c[0] == 'E'){ //Avanza y gira a la derecha
        //Direccion motor A
        digitalWrite (M1, LOW);
        analogWrite (E1,100); //Velocidad motor A
        //Direccion motor B
        digitalWrite (M2, HIGH);
        analogWrite (E2,150); //Velocidad motor B
    }
    else if (c[0] == 'Z') { //Izquierda y atrás
        //Direccion motor A
        digitalWrite (M1, HIGH);
        analogWrite (E1,150); //Velocidad motor A
        //Direccion motor B
        digitalWrite (M2, LOW);
        analogWrite (E2,100); //Velocidad motor B

    }
    else if (c[0] == 'C'){ //Atrás y derecha
        //Direccion motor A
        digitalWrite (M1, HIGH);
        analogWrite (E1,100); //Velocidad motor A
        //Direccion motor B
        digitalWrite (M2, LOW);
        analogWrite (E2,150); //Velocidad motor B
    }
    else if (c[0] == 'X') { //Parar
        //Direccion motor A
        digitalWrite (M1, LOW);
        analogWrite (E1,0); //Velocidad motor A
        //Direccion motor B
        digitalWrite (M2, HIGH);
        analogWrite (E2,0); //Velocidad motor B
    }
    else if (c[0] == 'T'){ //Turbo
        //Direccion motor A
        digitalWrite (M1, LOW);
        analogWrite (E1,250); //Velocidad motor A
        //Direccion motor B
        digitalWrite (M2, HIGH);
        analogWrite (E2,250); //Velocidad motor B
    }
    else {
       digitalWrite(noentra,HIGH);
       delay(2000);
    }
   
}
/*
 * Автор: Алексей Валуев.
 * Дата создания: 15.06.2017.
 * Описание: Скрипт для управления колёсным Arduino-роботом с управляемым держателем смартфона с помощью приложения RoboCam.
 * Приложение RoboCam в Google Play: https://play.google.com/store/apps/details?id=ru.proghouse.robocam
 * Статьи о приложении RoboCam: http://www.proghouse.ru/tags/robocam
*/

#include <math.h>

//------------------------------------------------------------------
// Функции для чтения сообщений RoboCam.
//------------------------------------------------------------------

//Команды RoboCam, которые приходят со смартфона.
const byte CMD_START    = 0;    //Команда "Старт".
const byte CMD_CALLSIGN = 1;    //Позывной.
const byte CMD_CTRL     = 2;    //Изменение состояния контроллеров (джойстиков и/или клавиш).
const byte CMD_TEST     = 3;    //Тест соединения.
const byte CMD_STOP     = 255;  //Команда "Стоп".

//Оси джойтиков.
const byte AXIS_X = 0;
const byte AXIS_Y = 1;
const byte AXIS_W = 2;
const byte AXIS_Z = 3;
const byte AXIS_A = 4;
const byte AXIS_B = 5;
const byte AXIS_C = 6;
const byte AXIS_D = 7;

//Клавиши, которые нас интересуют.
//Клавиши вперёд.
const byte VK_W     = 87;
const byte VK_UP    = 38;
//Клавиши налево.
const byte VK_A     = 65;
const byte VK_LEFT  = 37;
//Клавиши назад.
const byte VK_S     = 83;
const byte VK_DOWN  = 40;
//Клавиши направо.
const byte VK_D     = 68;
const byte VK_RIGHT = 39;
//Клавиша смотреть наверх.
const byte VK_Y     = 89;
//Клавиша смотреть вниз.
const byte VK_H     = 72;

//Состояние клавиши.
const byte KEY_PRESSED  = 255; //Клавиша нажата.
const byte KEY_RELEASED = 254; //Клавиша не нажата.

unsigned int messageSize = 0;
unsigned int readMessageBytes = 0;
byte message[255];
bool messageIsTooBig = false;

//Считыает сообщение RoboCam из последовательного порта.
bool readMessage()
{
  //Читаем размер сообщения.
  if (messageSize == 0 && Serial.available() > 1)
  {
    messageSize = Serial.read() + (Serial.read() << 8);
    readMessageBytes = 0;
  }

  //Считыаем сообщение.
  //Сообщение забираем из Serial полностью, даже если оно больше массива "message".
  //Если сообщение больше массива "message", выставляем флаг messageIsTooBig в true.
  if (messageSize > 0 && readMessageBytes < messageSize && Serial.available() > 0)
    while (readMessageBytes < messageSize && Serial.available() > 0)
    {
      byte b = Serial.read();
      if (readMessageBytes < sizeof(message))
        message[readMessageBytes] = b;
      else
        messageIsTooBig = true;
      readMessageBytes++;
    }

   return messageSize > 0 && readMessageBytes == messageSize;
}

//Удаляет сообщение.
void deleteMessage()
{
  messageSize = 0;
}

//Получает команду из сообщения.
byte getCommand()
{
  return message[0];
}

//Получает строку из сообщения.
String getString(unsigned int index)
{
  return (char*)&message[index];
}

//Возвращает значение беззнакового байта.
byte getUByte(unsigned int index)
{
  return message[index];
}

//Возвращает значение знакового байта.
int getSByte(unsigned int index)
{
  return message[index] > 127 ? message[index] - 256 : message[index];
}

unsigned int controllerIndex = 1;

//Начинает перечисление контроллеров.
void beginControllerEnumeration()
{
  controllerIndex = 1;
}

//Проверяет есть ли ещё контроллеры в перечислении.
bool hasController()
{
  return controllerIndex < messageSize;
}

//Передвигается к следующему контроллеру в перечислении.
void gotoNextController()
{
  if (isJoystickAxis() || isKey())
    controllerIndex += 2;
}

//Возвращает true, если контроллер - это клавиша.
bool isKey()
{
  return message[controllerIndex] == KEY_PRESSED || message[controllerIndex] == KEY_RELEASED;
}

//Возвращает true, если клавиши нажата.
bool isKeyPressed()
{
  return message[controllerIndex] == KEY_PRESSED;
}

//Возвращает true, если клавиши не нажата.
bool isKeyReleased()
{
  return message[controllerIndex] == KEY_RELEASED;
}

//Возвращает код клавиши.
byte getKeyCode()
{
  return isKey() ? message[controllerIndex + 1] : 0;
}

//Возвращает true, если текущий контроллер - это ось джойстика.
bool isJoystickAxis()
{
  return message[controllerIndex] < 8;
}

//Возвращает идентификатор оси джойстика.
byte getJoystickAxisId()
{
  return isJoystickAxis() ? message[controllerIndex] : -1;
}

String axisNames[] = {"x", "y", "w", "z", "a", "b", "c", "d"};

//Возвращает имя оси джойстика.
String getJoystickAxisName()
{
  return getJoystickAxisId() >= 0 ? axisNames[getJoystickAxisId()] : "";
}

//Возвращает значение по оси джойстика.
int getJoystickAxisValue()
{
  return isJoystickAxis() ? getSByte(controllerIndex + 1) : 0;
}


//------------------------------------------------------------------
// Функции для формирования и отправки ответов на сообщения RoboCam.
//------------------------------------------------------------------

unsigned int replySize = 0; //Размер ответа.
byte reply[20]; //Содержимое ответа. Длинных ответов у нас нет, поэтому хватит 20 байт.

//Создаёт новый ответ RoboCam.
void createReply()
{
  replySize = 0;
}

//Записывает беззнаковый байт в ответ.
void writeUByte(byte _byte)
{
  if (replySize < sizeof(reply))
    reply[replySize] = _byte;
   replySize++;
}

//Записывает строку в ответ.
void writeString(char* str)
{
  int index = 0;
  while (str[index] != 0)
  {
    writeUByte((byte)str[index]);
    index++;
  }
  writeUByte(0);
}

//Посылает ответ.
void sendReply()
{
  Serial.write(replySize & 0xFF);
  Serial.write((replySize >> 8) & 0xFF);
  Serial.write(reply, replySize);
}

//Создаёт и отправляет ответ, сообщая, что ошибок нет.
void createAndSendOKReply()
{
  createReply(); //Создаём ответ.
  writeUByte(0); //Ошибок нет.
  sendReply(); //Отправляем ответ.
}


//------------------------------------------------------------------
// Состояния джойстиков и клавиш.
//------------------------------------------------------------------

int joystickAxisValues[8];
bool pressedKeys[223];


//------------------------------------------------------------------
// Настройка моторов.
//------------------------------------------------------------------

int rDirPin = 4;
int rSpeedPin = 5;

int lSpeedPin = 6;
int lDirPin = 7;

int maxSpeed = 100;

int lSpeed = 0;
int rSpeed = 0;
int back = HIGH;
int forward = LOW;

void setupMotorShield()
{
    pinMode(rDirPin, OUTPUT);
    pinMode(rSpeedPin, OUTPUT);
    pinMode(lDirPin, OUTPUT);
    pinMode(lSpeedPin, OUTPUT);
}

void updateMotorStates()
{
  //Считаем скорость моторов в зависимости от координат по осям джойстиков x и y.
  int x = joystickAxisValues[AXIS_X];
  int y = joystickAxisValues[AXIS_Y];
  double angle = atan2(y, x) * 180.0 / M_PI;
  double d = sqrt(x * x + y * y); //Расстояние от центра окружности до точки
  if (d > 100)
      d = 100;
  double L = 0, R = 0;
  if (angle >= 0 && angle <= 90) {
      R = angle / 90 * 201 - 100;
      L = 100;
  } else if (angle < 0 && angle >= -90) {
      L = (angle / 90 * -201 - 100) * -1;
      R = -100;
  } else if (angle > 90 && angle <= 180) {
      L = ((angle - 90) / 90 * 201 - 100) * -1;
      R = 100;
  } else if (angle < -90 && angle >= -180) {
      R = (angle + 90) / 90 * -201 - 100;
      L = -100;
  }
  rSpeed = (int) round(maxSpeed * R / 100 * d / 100);
  lSpeed = (int) round(maxSpeed * L / 100 * d / 100);
  //Считаем скорость в зависимости от нажатых клавиш.
  int rSpeedBtn = 0;
  int lSpeedBtn = 0;
  bool up   = pressedKeys[VK_W] || pressedKeys[VK_UP];
  bool down = pressedKeys[VK_S] || pressedKeys[VK_DOWN];
  bool left = pressedKeys[VK_A] || pressedKeys[VK_LEFT];
  bool right = pressedKeys[VK_D] || pressedKeys[VK_RIGHT];
  if (up)
  {
    rSpeedBtn += maxSpeed;
    lSpeedBtn += maxSpeed;
  }
  if (down)
  {
    rSpeedBtn -= maxSpeed;
    lSpeedBtn -= maxSpeed;
  }
  if (left && !right)
    if (up || down)
      lSpeedBtn = 0;
    else
    {
      lSpeedBtn -= maxSpeed;
      rSpeedBtn += maxSpeed;
    }
  if (right && !left)
    if (up || down)
      rSpeedBtn = 0;
    else
    {
      lSpeedBtn += maxSpeed;
      rSpeedBtn -= maxSpeed;
    }
  rSpeed += rSpeedBtn;
  lSpeed += lSpeedBtn;
  rSpeed = max(min(rSpeed, maxSpeed), -maxSpeed);
  lSpeed = max(min(lSpeed, maxSpeed), -maxSpeed);
  updateMotorState(rDirPin, rSpeedPin, rSpeed);
  updateMotorState(lDirPin, lSpeedPin, lSpeed * -1);
}

void updateMotorState(int dirPin, int speedPin, int speed)
{
  if (speed == 0)
    analogWrite(speedPin, 0);
  else
  {
    analogWrite(speedPin, abs(speed));
    digitalWrite(dirPin, speed > 0 ? forward : back);
  }
}


//------------------------------------------------------------------
// Настройка сервомотора.
//------------------------------------------------------------------

#include <Servo.h>

Servo servo;
int servoMinAngle = 40;//Минимальный угол (>=0)
int servoMaxAngle = 140;//Максимальный угол (<=179)
int servoStep = 5;
unsigned long lastUpdate = 0;
unsigned long updatePeriod = 100;
int posByKeyboard = 0;

void setupServo()
{
  servo.attach(9);
  servo.write((servoMaxAngle - servoMinAngle) / 2);
}

void updateServoState()
{
  unsigned long currentTime = millis();
  //Считаем угол поворота сервомотора, в зависимости от координат джойстика.
  int posByJoystick = round((joystickAxisValues[AXIS_Z] + 100.0) * (servoMaxAngle - servoMinAngle) / 200.0) + servoMinAngle;
  //Если нажата клавиша Y или H и прошло более updatePeriod миллисекунд, считаем меняем относительный угол поворота.
  if (((pressedKeys[VK_Y] || pressedKeys[VK_H]) && pressedKeys[VK_Y] != pressedKeys[VK_H])
      && (lastUpdate == 0 || lastUpdate > currentTime || currentTime - lastUpdate > updatePeriod))
  {
    lastUpdate = currentTime;
    posByKeyboard += pressedKeys[VK_Y] ? servoStep : -servoStep;
    posByKeyboard = max(min(posByKeyboard, (servoMaxAngle - servoMinAngle) / 2), (servoMinAngle - servoMaxAngle) / 2);
  }
  //Считаем новый угол поворота сервомотора.
  int newPos = max(min(posByJoystick + posByKeyboard, servoMaxAngle), servoMinAngle);
  //Поворачиваем сервомотор.
  servo.write(newPos);
}

//------------------------------------------------------------------
// Основной код.
//------------------------------------------------------------------

void clearStoredValues()
{
  posByKeyboard = 0;
  for (int i = 0; i < sizeof(joystickAxisValues); i++)
    joystickAxisValues[i] = 0;
  for (int i = 0; i < sizeof(pressedKeys); i++)
    pressedKeys[i] = false;
}

void setup()
{
  clearStoredValues();
  setupMotorShield();
  setupServo();
  Serial.begin(9600);
}

void loop() 
{
  if (readMessage())
  {
    switch (getCommand())
    {
      case CMD_START: //Начало работы.
        //Создаём ответ.
        createReply();
        //Ошибок нет.
        writeUByte(0);
        //Контрольный байт. Нужно вернуть полученное значение увеличенное на 1.
        writeUByte(message[1] + 1);
        //Версия протокола общения, которую мы будем использовать.
        writeUByte(1);
        //Кодировка для строк US-ASCII.
        writeUByte(0);
        //Отправляем ответ.
        sendReply();
        break;
      case CMD_CALLSIGN: //Запрос отзыва на позывной.
        //Создаём ответ.
        createReply();
        if (getString(1) == "RoboCam") //Если позывной "RoboCam"...
        {
          //Ошибок нет.
          writeUByte(0);
          //Ответ "Researcher".
          writeString("Researcher");
        }
        else
          //Ошибка, т.к. получен неправильный позывной.
          writeUByte(1);
        //Отправляем ответ.
        sendReply();
        break;
      case CMD_CTRL: //Изменения состояний контроллеров.
        beginControllerEnumeration(); //Создаём перечисление состояний контроллеров.
        while (hasController()) //Если есть контроллер.
        {
          if (isJoystickAxis()) //Если контроллер - это ось джойстика.
            joystickAxisValues[getJoystickAxisId()] = getJoystickAxisValue();
          else if (isKey()) //Если контроллер - это клавиша.
          {
            if (isKeyPressed()) //Если клавиша нажата.
              pressedKeys[getKeyCode()] = true;
            else if (isKeyReleased()) //Если клавиша не нажата.
              pressedKeys[getKeyCode()] = false;
          }
          gotoNextController(); //Переходим к следующему контролеру.
        }
        //Обновляем состояния моторов.
        updateMotorStates();
        //Отправляем ответ.
        createAndSendOKReply();
        break;
      case CMD_TEST: //Проверка подключения.
        //Отправляем ответ.
        createAndSendOKReply();
        break;
      case CMD_STOP: //Остановка робота.
        //Обнуляем координаты осей джойстиков и состояния клавиш.
        clearStoredValues();
        //Обновляем состояния моторов.
        updateMotorStates();
        //Отправляем ответ.
        createAndSendOKReply();
        break;
    }
    //Удаляем сообщение.
    deleteMessage();
  }
  //Обновляем состояние сервомотора.
  updateServoState();
}

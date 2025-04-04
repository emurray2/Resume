// See ESP32Wiimote submodule for included libraries
#include "ESP32Wiimote.h"

ESP32Wiimote wiimote;

void setup()
{
    Serial.begin(115200);
    Serial.println("ESP32Wiimote");
    wiimote.init();
    Serial.println("Started");
}

void loop()
{
    wiimote.task();
    if (wiimote.available() > 0) 
    {
        ButtonState  button  = wiimote.getButtonState();
        AccelState   accel   = wiimote.getAccelState();
        NunchukState nunchuk = wiimote.getNunchukState();
        char ca     = (button & BUTTON_A)     ? 'A' : '.';
        char cb     = (button & BUTTON_B)     ? 'B' : '.';
        char cc     = (button & BUTTON_C)     ? 'C' : '.';
        char cz     = (button & BUTTON_Z)     ? 'Z' : '.';
        char c1     = (button & BUTTON_ONE)   ? '1' : '.';
        char c2     = (button & BUTTON_TWO)   ? '2' : '.';
        char cminus = (button & BUTTON_MINUS) ? '-' : '.';
        char cplus  = (button & BUTTON_PLUS)  ? '+' : '.';
        char chome  = (button & BUTTON_HOME)  ? 'H' : '.';
        char cleft  = (button & BUTTON_LEFT)  ? '<' : '.';
        char cright = (button & BUTTON_RIGHT) ? '>' : '.';
        char cup    = (button & BUTTON_UP)    ? '^' : '.';
        char cdown  = (button & BUTTON_DOWN)  ? 'v' : '.';
        // Serial.printf("button: %05x = ", (int)button);
        Serial.print(ca);
        Serial.print(" ");
        Serial.print(cb);
        Serial.print(" ");
        Serial.print(cc);
        Serial.print(" ");
        Serial.print(cz);
        Serial.print(" ");
        Serial.print(c1);
        Serial.print(" ");
        Serial.print(c2);
        Serial.print(" ");
        Serial.print(cminus);
        Serial.print(" ");
        Serial.print(chome);
        Serial.print(" ");
        Serial.print(cplus);
        Serial.print(" ");
        Serial.print(cleft);
        Serial.print(" ");
        Serial.print(cright);
        Serial.print(" ");
        Serial.print(cup);
        Serial.print(" ");
        Serial.print(cdown);
        Serial.print(" ");
        Serial.print(accel.xAxis);
        Serial.print(" ");
        Serial.print(accel.yAxis);
        Serial.print(" ");
        Serial.print(accel.zAxis);
        Serial.print(" ");
        Serial.print(nunchuk.xAxis);
        Serial.print(" ");
        Serial.print(nunchuk.yAxis);
        Serial.print(" ");
        Serial.print(nunchuk.zAxis);
        Serial.print(" ");
        Serial.print(nunchuk.xStick);
        Serial.print(" ");
        Serial.print(nunchuk.yStick);
        Serial.println();
    }
    delay(10);
}

#include <stdio.h>
#include <string.h>
#include <tusb.h>

#include "pico/stdlib.h"
#include "pico/binary_info.h"

//Testing communication with HID Device over usb

int main() 
{
    stdio_init_all();

    //Set LED as output for testing purposes
    gpio_init(13);
    gpio_set_dir(13, GPIO_OUT);

    char userIn;

    while(1)
    {
        


        printf("ON OR OFF\n");
        userIn = getchar();
        //initial test with my UF ISO : Jonathan
        if(userIn == '6')
        {
            gpio_put(13,1);
            printf("LED ON\n");
        }
        else if(userIn == '0')
        {
            gpio_put(13,0);
            printf("OFF\n");
        }
        else{
            gpio_put(13,1);
            printf("INVALID\n");
        }
    }
}
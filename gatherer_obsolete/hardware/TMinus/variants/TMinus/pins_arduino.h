/*
  
  Remake of the Pins_arduino.h for the T-Minus board.
  
  
  
  
  pins_arduino.h - Pin definition functions for Arduino
  Part of Arduino - http://www.arduino.cc/

  Copyright (c) 2007 David A. Mellis

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General
  Public License along with this library; if not, write to the
  Free Software Foundation, Inc., 59 Temple Place, Suite 330,
  Boston, MA  02111-1307  USA

  $Id: wiring.h 249 2007-02-03 16:52:51Z mellis $
*/

#ifndef Pins_Arduino_h
#define Pins_Arduino_h

#include <avr/pgmspace.h>

#define NUM_DIGITAL_PINS            56
#define NUM_ANALOG_INPUTS           12
#define analogInputToDigitalPin(p)  ((p < 12) ? (p) + 40 : -1)
#define digitalPinHasPWM(p)         (((p) >= 3 && (p) <= 6) || ((p) >= 11 && (p)<= 13) || ((p) == 29) || ((p) == 31) || ((p) == 53))

const static uint8_t SS   = 27;
const static uint8_t MOSI = 25;
const static uint8_t MISO = 24;
const static uint8_t SCK  = 26;

const static uint8_t SDA = 32;
const static uint8_t SCL = 33;
const static uint8_t LED_BUILTIN = 16;
const static uint8_t LED_BUILTIN1 = 17;
const static uint8_t LED_BUILTIN2 = 18;
const static uint8_t LED_BUILTIN3 = 19;
const static uint8_t LED_BUILTIN4 = 20;
const static uint8_t LED_BUILTIN5 = 21;
const static uint8_t LED_BUILTIN6 = 22;
const static uint8_t LED_BUILTIN7 = 23;

const static uint8_t A0 = 40;
const static uint8_t A1 = 41;
const static uint8_t A2 = 42;
const static uint8_t A3 = 43;
const static uint8_t A4 = 44;
const static uint8_t A5 = 45;
const static uint8_t A6 = 46;
const static uint8_t A7 = 47;
const static uint8_t A8 = 48;
const static uint8_t A9 = 49;
const static uint8_t A10 = 50;
const static uint8_t A11 = 51;

// A majority of the pins are NOT PCINTs, SO BE WARNED (i.e. you cannot use them as receive pins)
// Only pins available for RECEIVE (TRANSMIT can be on any pin):
// (I've deliberately left out pin mapping to the Hardware USARTs - seems senseless to me)
// Pins: 10, 11, 12, 13,  50, 51, 52, 53,  62, 63, 64, 65, 66, 67, 68, 69

// next 4 lines are still to be updated

#define digitalPinToPCICR(p)    ( (((p) >= 10) && ((p) <= 13)) || \
                                  (((p) >= 50) && ((p) <= 53)) || \
                                  (((p) >= 62) && ((p) <= 69)) ? (&PCICR) : ((uint8_t *)0) )

#define digitalPinToPCICRbit(p) ( (((p) >= 10) && ((p) <= 13)) || (((p) >= 50) && ((p) <= 53)) ? 0 : \
                                ( (((p) >= 62) && ((p) <= 69)) ? 2 : \
                                0 ) )

#define digitalPinToPCMSK(p)    ( (((p) >= 10) && ((p) <= 13)) || (((p) >= 50) && ((p) <= 53)) ? (&PCMSK0) : \
                                ( (((p) >= 62) && ((p) <= 69)) ? (&PCMSK2) : \
                                ((uint8_t *)0) ) )

#define digitalPinToPCMSKbit(p) ( (((p) >= 10) && ((p) <= 13)) ? ((p) - 6) : \
                                ( ((p) == 50) ? 3 : \
                                ( ((p) == 51) ? 2 : \
                                ( ((p) == 52) ? 1 : \
                                ( ((p) == 53) ? 0 : \
                                ( (((p) >= 62) && ((p) <= 69)) ? ((p) - 62) : \
                                0 ) ) ) ) ) )

#ifdef ARDUINO_MAIN

const uint16_t PROGMEM port_to_mode_PGM[] = {
	NOT_A_PORT,
	(uint16_t) &DDRA,
	(uint16_t) &DDRB,
	(uint16_t) &DDRC,
	(uint16_t) &DDRD,
	(uint16_t) &DDRE,
	(uint16_t) &DDRF,
	(uint16_t) &DDRG,
	(uint16_t) &DDRH,
	NOT_A_PORT,
	(uint16_t) &DDRJ,
	(uint16_t) &DDRK,
	(uint16_t) &DDRL,
};

const uint16_t PROGMEM port_to_output_PGM[] = {
	NOT_A_PORT,
	(uint16_t) &PORTA,
	(uint16_t) &PORTB,
	(uint16_t) &PORTC,
	(uint16_t) &PORTD,
	(uint16_t) &PORTE,
	(uint16_t) &PORTF,
	(uint16_t) &PORTG,
	(uint16_t) &PORTH,
	NOT_A_PORT,
	(uint16_t) &PORTJ,
	(uint16_t) &PORTK,
	(uint16_t) &PORTL,
};

const uint16_t PROGMEM port_to_input_PGM[] = {
	NOT_A_PIN,
	(uint16_t) &PINA,
	(uint16_t) &PINB,
	(uint16_t) &PINC,
	(uint16_t) &PIND,
	(uint16_t) &PINE,
	(uint16_t) &PINF,
	(uint16_t) &PING,
	(uint16_t) &PINH,
	NOT_A_PIN,
	(uint16_t) &PINJ,
	(uint16_t) &PINK,
	(uint16_t) &PINL,
};

const uint8_t PROGMEM digital_pin_to_port_PGM[] = {
	// PORTLIST		
	// -------------------------------------------		
	PH	, // PH 0 ** 0 ** 
	PH	, // PH 1 ** 1 ** 	
	PH	, // PH 2 ** 2 ** 	
	PH	, // PH 3 ** 3 ** 	
	PH	, // PH 4 ** 4 ** 	
	PH	, // PH 5 ** 5 **	
	PH	, // PH 6 ** 6 ** 	
	PH	, // PH 7 ** 7 ** 	
	PL	, // PL 0 ** 8 ** 	
	PL	, // PL 1 ** 9 **	
	PL	, // PL 2 ** 10 ** 	
	PL	, // PL 3 ** 11 **	
	PL	, // PL 4 ** 12 ** 	
	PL	, // PL 5 ** 13 ** 	
	PL	, // PL 6 ** 14 ** 	
	PL	, // PL 7 ** 15 ** 	
	PA	, // PA 0 ** 16 ** 	
	PA	, // PA 1 ** 17 ** 	
	PA	, // PA 2 ** 18 ** 	
	PA	, // PA 3 ** 19 ** 	
	PA	, // PA 4 ** 20 ** 
	PA	, // PA 5 ** 21 ** 	
	PA	, // PA 6 ** 22 **
	PA	, // PA 7 ** 23 **
	PB	, // PB 3 ** 24 ** 
	PB	, // PB 2 ** 25 ** 
	PB	, // PB 1 ** 26 **
	PB	, // PB 0 ** 27 ** 
	PD	, // PD 7 ** 28 **
	PB	, // PB 7 ** 29 ** 
	PD	, // PD 6 ** 30 ** 
	PB	, // PB 5 ** 31 ** 
	PD	, // PD 1 ** 32 ** 
	PD	, // PD 0 ** 33 ** 
	PD	, // PD 2 ** 34 ** 
	PD	, // PD 3 ** 35 ** 
	PD	, // PD 5 ** 36 ** 
	PJ	, // PJ 0 ** 37 ** 
	PJ	, // PJ 1 ** 38 ** 
	PJ	, // PJ 2 ** 39 ** 
	PF	, // PF 0 ** 40 ** 
	PF	, // PF 1 ** 41 ** 
	PF	, // PF 2 ** 42 ** 
	PF	, // PF 3 ** 43 ** 
	PK	, // PK 0 ** 44 ** 
	PK	, // PK 1 ** 45 ** 
	PK	, // PK 2 ** 46 ** 	
	PK	, // PK 3 ** 47 ** 	
	PK	, // PK 4 ** 48 ** 	
	PK	, // PK 5 ** 49 ** 	
	PK	, // PK 6 ** 50 ** 	
	PK	, // PK 7 ** 51 ** 	
	PE	, // PB 2 ** 52 ** 	
	PE	, // PB 3 ** 53 ** 	
	PE	, // PF 0 ** 54 ** 
	PE	, // PF 1 ** 55 ** 
};

const uint8_t PROGMEM digital_pin_to_bit_mask_PGM[] = {
	// PIN IN PORT		
	// -------------------------------------------		
	_BV( 0 )	, // PH 0 ** 0 ** 
	_BV( 1 )	, // PH 1 ** 1 ** 	
	_BV( 2 )	, // PH 2 ** 2 ** 	
	_BV( 3 )	, // PH 3 ** 3 ** 	
	_BV( 4 )	, // PH 4 ** 4 ** 	
	_BV( 5 )	, // PH 5 ** 5 **	
	_BV( 6 )	, // PH 6 ** 6 ** 	
	_BV( 7 )	, // PH 7 ** 7 ** 	
	_BV( 0 )	, // PL 0 ** 8 ** 	
	_BV( 1 )	, // PL 1 ** 9 **	
	_BV( 2 )	, // PL 2 ** 10 ** 	
	_BV( 3 )	, // PL 3 ** 11 **	
	_BV( 4 )	, // PL 4 ** 12 ** 	
	_BV( 5 )	, // PL 5 ** 13 ** 	
	_BV( 6 )	, // PL 6 ** 14 ** 	
	_BV( 7 )	, // PL 7 ** 15 ** 	
	_BV( 0 )	, // PA 0 ** 16 ** 	
	_BV( 1 )	, // PA 1 ** 17 ** 	
	_BV( 2 )	, // PA 2 ** 18 ** 	
	_BV( 3 )	, // PA 3 ** 19 ** 	
	_BV( 4 )	, // PA 4 ** 20 ** 
	_BV( 5 )	, // PA 5 ** 21 ** 	
	_BV( 6 )	, // PA 6 ** 22 **
	_BV( 7 )	, // PA 7 ** 23 **
	_BV( 3 )	, // PB 3 ** 24 ** 
	_BV( 2 )	, // PB 2 ** 25 ** 
	_BV( 1 )	, // PB 1 ** 26 **
	_BV( 0 )	, // PB 0 ** 27 ** 
	_BV( 7 )	, // PD 7 ** 28 **
	_BV( 7 )	, // PB 7 ** 29 ** 
	_BV( 6 )	, // PD 6 ** 30 ** 
	_BV( 5 )	, // PB 5 ** 31 ** 
	_BV( 1 )	, // PD 1 ** 32 ** 
	_BV( 0 )	, // PD 0 ** 33 ** 
	_BV( 2 )	, // PD 2 ** 34 ** 
	_BV( 3 )	, // PD 3 ** 35 ** 
	_BV( 5 )	, // PD 5 ** 36 ** 
	_BV( 0 )	, // PJ 0 ** 37 ** 
	_BV( 1 )	, // PJ 1 ** 38 ** 
	_BV( 2 )	, // PJ 2 ** 39 ** 
	_BV( 0 )	, // PF 0 ** 40 ** 
	_BV( 1 )	, // PF 1 ** 41 ** 
	_BV( 2 )	, // PF 2 ** 42 ** 
	_BV( 3 )	, // PF 3 ** 43 ** 
	_BV( 0 )	, // PK 0 ** 44 ** 
	_BV( 1 )	, // PK 1 ** 45 ** 
	_BV( 2 )	, // PK 2 ** 46 ** 	
	_BV( 3 )	, // PK 3 ** 47 ** 	
	_BV( 4 )	, // PK 4 ** 48 ** 	
	_BV( 5 )	, // PK 5 ** 49 ** 	
	_BV( 6 )	, // PK 6 ** 50 ** 	
	_BV( 7 )	, // PK 7 ** 51 ** 	
	_BV( 2 )	, // PB 2 ** 52 ** 	
	_BV( 3 )	, // PB 3 ** 53 ** 	
	_BV( 0 )	, // PF 0 ** 54 ** 
	_BV( 1 )	, // PF 1 ** 55 ** 
};

const uint8_t PROGMEM digital_pin_to_timer_PGM[] = {
	// TIMERS		
	// -------------------------------------------		
	NOT_ON_TIMER	, // PH 0 ** 0 ** 
	NOT_ON_TIMER	, // PH 1 ** 1 ** 	
	NOT_ON_TIMER	, // PH 2 ** 2 ** 	
	TIMER4A			, // PH 3 ** 3 ** 	
	TIMER4B			, // PH 4 ** 4 ** 	
	TIMER4C			, // PH 5 ** 5 **	
	TIMER2B			, // PH 6 ** 6 ** 	
	NOT_ON_TIMER	, // PH 7 ** 7 ** 	
	NOT_ON_TIMER	, // PL 0 ** 8 ** 	
	NOT_ON_TIMER	, // PL 1 ** 9 **	
	NOT_ON_TIMER	, // PL 2 ** 10 ** 	
	TIMER5A			, // PL 3 ** 11 **	
	TIMER5B			, // PL 4 ** 12 ** 	
	TIMER5C			, // PL 5 ** 13 ** 	
	NOT_ON_TIMER	, // PL 6 ** 14 ** 	
	NOT_ON_TIMER	, // PL 7 ** 15 ** 	
	NOT_ON_TIMER	, // PA 0 ** 16 ** 	
	NOT_ON_TIMER	, // PA 1 ** 17 ** 	
	NOT_ON_TIMER	, // PA 2 ** 18 ** 	
	NOT_ON_TIMER	, // PA 3 ** 19 ** 	
	NOT_ON_TIMER	, // PA 4 ** 20 ** 
	NOT_ON_TIMER	, // PA 5 ** 21 ** 	
	NOT_ON_TIMER	, // PA 6 ** 22 **
	NOT_ON_TIMER	, // PA 7 ** 23 **
	NOT_ON_TIMER	, // PB 3 ** 24 ** 
	NOT_ON_TIMER	, // PB 2 ** 25 ** 
	NOT_ON_TIMER	, // PB 1 ** 26 **
	NOT_ON_TIMER	, // PB 0 ** 27 ** 
	NOT_ON_TIMER	, // PD 7 ** 28 **
	TIMER0A			, // PB 7 ** 29 ** 
	NOT_ON_TIMER	, // PD 6 ** 30 ** 
	TIMER1A			, // PB 5 ** 31 ** 
	NOT_ON_TIMER	, // PD 1 ** 32 ** 
	NOT_ON_TIMER	, // PD 0 ** 33 ** 
	NOT_ON_TIMER	, // PD 2 ** 34 ** 
	NOT_ON_TIMER	, // PD 3 ** 35 ** 
	NOT_ON_TIMER	, // PD 5 ** 36 ** 
	NOT_ON_TIMER	, // PJ 0 ** 37 ** 
	NOT_ON_TIMER	, // PJ 1 ** 38 ** 
	NOT_ON_TIMER	, // PJ 2 ** 39 ** 
	NOT_ON_TIMER	, // PF 0 ** 40 ** 
	NOT_ON_TIMER	, // PF 1 ** 41 ** 
	NOT_ON_TIMER	, // PF 2 ** 42 ** 
	NOT_ON_TIMER	, // PF 3 ** 43 ** 
	NOT_ON_TIMER	, // PK 0 ** 44 ** 
	NOT_ON_TIMER	, // PK 1 ** 45 ** 
	NOT_ON_TIMER	, // PK 2 ** 46 ** 	
	NOT_ON_TIMER	, // PK 3 ** 47 ** 	
	NOT_ON_TIMER	, // PK 4 ** 48 ** 	
	NOT_ON_TIMER	, // PK 5 ** 49 ** 	
	NOT_ON_TIMER	, // PK 6 ** 50 ** 	
	NOT_ON_TIMER	, // PK 7 ** 51 ** 	
	NOT_ON_TIMER	, // PB 2 ** 52 ** 	
	TIMER3A			, // PB 3 ** 53 ** 	
	NOT_ON_TIMER	, // PF 0 ** 54 ** 
	NOT_ON_TIMER	, // PF 1 ** 55 ** 
};

#endif

#endif
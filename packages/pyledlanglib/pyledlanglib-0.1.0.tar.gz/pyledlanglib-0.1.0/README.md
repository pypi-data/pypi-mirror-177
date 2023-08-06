# PyLEDLang
The simple amazing software for RGB lights.

# Explaination.
The compiler is an small python lib that converts your amazing python code to an PyLEDasm (text lang that led controller will understand).
So it does an magic :)
It can convert this 
```
from code import Compiler

def main():
	x=Compiler()
	for a in range(0,10):
				x.set_color(a*25,a*25,a*25)
				x.sleep(20)
	x.final_build()
pass
main()
```
In to:
```
;user defined color from hex 0 0 0
reg clr:000000
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
;user defined color from hex 25 25 25
reg clr:191919
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
;user defined color from hex 50 50 50
reg clr:323232
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
;user defined color from hex 75 75 75
reg clr:4B4B4B
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
;user defined color from hex 100 100 100
reg clr:646464
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
;user defined color from hex 125 125 125
reg clr:7D7D7D
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
;user defined color from hex 150 150 150
reg clr:969696
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
;user defined color from hex 175 175 175
reg clr:AFAFAF
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
;user defined color from hex 200 200 200
reg clr:C8C8C8
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
;user defined color from hex 225 225 225
reg clr:E1E1E1
;user defined delay block via sleep method: 20 cycles
slp:00 -> sleep
```


To do it just an run your main.py in console.
``` py main.py output_final.bin True ```
Where output_final.bin is output filename and True is an for including an debug info.

![image](https://user-images.githubusercontent.com/20460747/202704599-f268c928-8040-4ded-ac4f-d72f916202d1.png)

# PyLEDasm rules:
1) All comments starts with ;
2) reg clr changes an color on output of /dev/color_rgb
3) slp:00 -> sleep delays an programm for one cylce.


'''Strings, each defining a macro used by the gerber_writer'''
# Copyright: Karel Tavernier
# Date: 20-Jun-2022
# License: Apache 2.0 License
#
# Revision history

_MACRO_RECTANGLE = '''%AMRectangle*
0 Rectangle with straight corners*
0 Uses primitive 4 only, without calculations*
0 $1 xsize/2*
0 $2 ysize/2*
0 $3 rotation angle*
4,1,4,
$1,$2,
$1,-$2,
-$1,-$2,
-$1,$2,
$1,$2,
$3*
%'''

_MACRO_CHAMFERED_RECTANGLE = '''%AMChamferedRectangle*
0 Rectangle with chamfered corners*
0 Uses primitive 4 only, without calculations*
0 $1 xsize/2*
0 $2 ysize/2*
0 $3 xsize/2-cutoff*
0 $y size/2-cutoff*
0 $5 rotation angle*
4,1,8,
$3,$2,
$1,$4,
$1,-$4,
$3,-$2,
-$3,-$2,
-$1,-$4,
-$1,$4,
-$3,$2,
$3,$2,
$5*
%'''

_MACRO_ROUNDED_RECTANGLE = '''%AMRoundedRectangle*
0 Rectangle with rounded corners*
0 Uses primitive 1 and 4 only, without calculations*
0 $1 xsize/2*
0 $2 ysize/2*
0 $3 xsize/2-radius*
0 $4 size/2-radius*
0 $5 rotation angle*
0 $6 diameter*
0 $7 x of center of first quadrant circle*
0 $8 y of center of first quadrant circle*
0 $9 x of center of 2nd quadrant circle*
0 $10 y of center of 2nd quadrant circle*
4,1,8,
$3,$2,
$1,$4,
$1,-$4,
$3,-$2,
-$3,-$2,
-$1,-$4,
-$1,$4,
-$3,$2,
$3,$2,
$5*
1,1,$6,$7,$8*
1,1,$6,-$7,-$8*
1,1,$6,$9,$10*
1,1,$6,-$9,-$10*
%'''

_MACRO_THERMAL = '''%AMThermal*
0 Circular thermal with straight corners*
0 $1 outer diameter*
0 $2 inner diameter*
0 $3 gap
0 $4 rotation angle*
7,0,0,$1,$2,$3,$4*
%'''

_MACRO_ROUNDED_THERMAL = '''%AMRoundedThermal*
0 Circular thermal with rounded corners*
0 $1 outer diameter*
0 $2 inner diameter*
0 $3 gap of straight thermal primitive*
0 $4 rotation angle*
0 $5 diameter rounding circles*
0 $6 x coordinate of q1 along h axis circle, rotated*
0 $7 y coordinate of q1 along h axis circle, rotated*
0 $8 x coordinate of q1 along v axis circle, rotated*
0 $9 y coordinate of q1 along v axis circle, rotated*
7,0,0,$1,$2,$3,$4*
1,1,$5,$6,$7*
1,1,$5,-$7,$6*
1,1,$5,-$6,-$7*
1,1,$5,$7,-$6*
1,1,$5,$8,$9*
1,1,$5,-$9,$8*
1,1,$5,-$8,-$9*
1,1,$5,$9,-$8*
1,0,$2,0,0*
%'''
***************************************************************************
* test1.sp
***************************************************************************
.subckt opamp_test_case_1 VDDR VSSA i50ua out vinn vinp
* port INPUT VDDR VSSA i50ua vinn vinp
* port OUTPUT out
MMXM11 biasp1 i50ua VSSA VSSA nch_18_mac l=2e-07 m=1 nf=5 nfin=20 w=4.61e-06
.ends opamp_test_case_1

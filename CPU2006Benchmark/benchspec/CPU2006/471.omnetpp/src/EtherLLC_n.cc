//-----------------------------------------
//
// Generated by NEDC version 2.3
// date:	Tue May 18 19:06:57 2004
//
// Input file:	EtherLLC.ned
// Output file:	EtherLLC_n.cc
//-----------------------------------------


#if defined(SPEC_CPU)
#include <cmath>
#else
#include <math.h>
#endif
#include "omnetpp.h"

#define check_error() \
    {(void)0;}
#define check_memory() \
    {if (memoryIsLow()) {throw new cException(eNOMEM); }}
#define check_module_count(num, mod, parentmod) \
    {if ((int)num<=0) {throw new cException("Negative or zero module vector size %s[%d] in compound module %s", \
                          mod,(int)num,parentmod);}}
#define check_gate_count(num, mod, gate, parentmod) \
    {if ((int)num<0) {throw new cException("Negative gate vector size %s.%s[%d] in compound module %s", \
                          mod,gate,(int)num,parentmod);}}
#define check_loop_bounds(lower, upper, parentmod) \
    {if ((int)lower<0) \
        {throw new cException("Bad loop bounds (%d..%d) in compound module %s", \
                 (int)lower,(int)upper,parentmod);}}
#define check_module_index(index,modvar,modname,parentmod) \
    {if (index<0 || index>=modvar[0]->size()) {throw new cException("Bad submodule index %s[%d] in compound module %s", \
          modname,(int)index,parentmod);}}
#define check_channel_params(delay, err, channel) \
    {if ((double)delay<0.0) \
        {throw new cException("Negative delay value %lf in channel %s",(double)delay,channel);} \
     if ((double)err<0.0 || (double)err>1.0) \
        {throw new cException("Incorrect error value %lf in channel %s",(double)err,channel);}}
#define check_modtype(modtype, modname) \
    {if ((modtype)==NULL) {throw new cException("Simple module type definition %s not found", \
                                     modname);}}
#define check_function(funcptr, funcname) \
    {if ((funcptr)==NULL) {throw new cException("Function %s not found", \
                                     funcname);}}
#define check_function_retnull(funcptr, funcname) \
    {if ((funcptr)==NULL) {throw new cException("Function %s not found", \
                                     funcname);return NULL;}}
#define check_gate(gateindex, modname, gatename) \
    {if ((int)gateindex==-1) {throw new cException("Gate %s.%s not found",modname,gatename);}}
#define check_anc_param(ptr,parname,compoundmod) \
    {if ((ptr)==NULL) {throw new cException("Unknown ancestor parameter named %s in compound module %s", \
                                parname,compoundmod);}}
#define check_param(ptr,parname) \
    {if ((ptr)==NULL) {throw new cException("Unknown parameter named %s", \
                                parname);}}
#ifndef __cplusplus
#  error Compile as C++!
#endif
#ifdef __BORLANDC__
#  if !defined(__FLAT__) && !defined(__LARGE__)
#    error Compile as 16-bit LARGE model or 32-bit DPMI!
#  endif
#endif

// Disable warnings about unused variables:
#ifdef _MSC_VER
#  pragma warning(disable:4101)
#endif
#ifdef __BORLANDC__
#  pragma warn -waus
#  pragma warn -wuse
#endif
// for GCC, seemingly there's no way to emulate the -Wunused command-line
// flag from a source file...

// Version check
#define NEDC_VERSION 0x0203
#if (NEDC_VERSION!=OMNETPP_VERSION)
#    error Version mismatch! Probably this file was generated by an earlier version of nedc: 'make clean' should help.
#endif

//--------------------------------------------
// Following code generated from: EtherLLC.ned
//--------------------------------------------

ModuleInterface( EtherLLC )
	Machine( default )
	Parameter( writeScalars, ParType_Bool )
	Gate( upperLayerIn[], GateDir_Input )
	Gate( upperLayerOut[], GateDir_Output )
	Gate( lowerLayerIn, GateDir_Input )
	Gate( lowerLayerOut, GateDir_Output )
EndInterface

Register_ModuleInterface( EtherLLC )

// class EtherLLC : public cSimpleModule
// {
//     Module_Class_Members(EtherLLC,cSimpleModule,8192)
//     virtual void activity();
//     // Add you own member functions here!
// };
//
// Define_Module( EtherLLC )
//
// void EtherLLC::activity()
// {
//     // Put code for simple module activity here!
// }
//


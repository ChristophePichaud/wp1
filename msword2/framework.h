// framework.h : include file for standard system include files,
//  or project specific include files that are used frequently,
//  but are changed infrequently
#pragma once

#ifndef WINVER
#define WINVER 0x0A00
#endif

#ifndef _WIN32_WINNT
#define _WIN32_WINNT 0x0A00
#endif

#ifndef _WIN32_WINDOWS
#define _WIN32_WINDOWS 0x0410
#endif

#ifndef _WIN32_IE
#define _WIN32_IE 0x0700
#endif

#define _ATL_CSTRING_EXPLICIT_CONSTRUCTORS

#define VC_EXTRA_LEAN

#ifndef VC_EXTRA_LEAN
#define VC_EXTRA_LEAN
#endif

#include <afxwin.h>
#include <afxext.h>
#include <afxdisp.h>

#ifndef _AFX_NO_OLE_SUPPORT
#include <afxdtctl.h>
#endif
#ifndef _AFX_NO_AFXCMN_SUPPORT
#include <afxcmn.h>
#endif

#include <afxcontrolbars.h>
#include <afxwinappex.h>
#include <afxframewndex.h>
#include <afxmdiframewndex.h>
#include <afxdialogex.h>
#include <afxribbon.h>

// msword2.h : main header file for the msword2 application
#pragma once

#ifndef __AFXWIN_H__
    #error "include 'pch.h' before including this file for PCH"
#endif

#include "resource.h"

class CMsword2App : public CWinAppEx
{
public:
    CMsword2App() noexcept;

public:
    virtual BOOL InitInstance();
    virtual int ExitInstance();

    UINT m_nAppLook;
    virtual void PreLoadState();
    virtual void LoadCustomState();
    virtual void SaveCustomState();

    afx_msg void OnAppAbout();
    DECLARE_MESSAGE_MAP()
};

extern CMsword2App theApp;

// MainFrm.h : interface of the CMainFrame class
#pragma once

class CMainFrame : public CMDIFrameWndEx
{
    DECLARE_DYNAMIC(CMainFrame)
public:
    CMainFrame() noexcept;

    virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
    virtual BOOL LoadFrame(UINT nIDResource,
        DWORD dwDefaultStyle = WS_OVERLAPPEDWINDOW | FWS_ADDTOTITLE,
        CWnd* pParentWnd = nullptr,
        CCreateContext* pContext = nullptr);

protected:
    CMFCRibbonBar     m_wndRibbonBar;
    CMFCRibbonApplicationButton m_MainButton;
    CMFCToolBarImages m_PanelImages;
    CMFCRibbonStatusBar  m_wndStatusBar;

public:
    virtual ~CMainFrame();

protected:
    afx_msg int OnCreate(LPCREATESTRUCT lpCreateStruct);
    afx_msg void OnWindowManager();
    afx_msg void OnApplicationLook(UINT id);
    afx_msg void OnUpdateApplicationLook(CCmdUI* pCmdUI);
    afx_msg void OnSettingChange(UINT uFlags, LPCTSTR lpszSection);

    DECLARE_MESSAGE_MAP()
};

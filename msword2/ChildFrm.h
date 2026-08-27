// ChildFrm.h : interface of the CChildFrame class
#pragma once

class CChildFrame : public CMDIChildWndEx
{
    DECLARE_DYNCREATE(CChildFrame)
public:
    CChildFrame() noexcept;

    virtual BOOL PreCreateWindow(CREATESTRUCT& cs);

public:
    virtual ~CChildFrame();
#ifdef _DEBUG
    virtual void AssertValid() const;
    virtual void Dump(CDumpContext& dc) const;
#endif

    DECLARE_MESSAGE_MAP()
};

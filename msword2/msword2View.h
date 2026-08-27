// msword2View.h : interface of the CMsword2View class
#pragma once

class CMsword2View : public CView
{
protected:
    CMsword2View() noexcept;
    DECLARE_DYNCREATE(CMsword2View)

private:
    CString     m_strText;      // accumulated text
    int         m_nCaretX;      // caret X position in pixels
    int         m_nCaretY;      // caret Y position in pixels
    int         m_nLineHeight;  // height of a text line
    int         m_nCharWidth;   // average character width
    CFont       m_font;         // editing font

public:
    CMsword2Doc* GetDocument() const;
    virtual void OnDraw(CDC* pDC);
    virtual BOOL PreCreateWindow(CREATESTRUCT& cs);

protected:
    virtual void OnInitialUpdate();

    afx_msg void OnSetFocus(CWnd* pOldWnd);
    afx_msg void OnKillFocus(CWnd* pNewWnd);
    afx_msg void OnChar(UINT nChar, UINT nRepCnt, UINT nFlags);
    afx_msg void OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags);
    afx_msg void OnSize(UINT nType, int cx, int cy);

    void UpdateCaretPos();
    void RecalcMetrics(CDC* pDC);

public:
    virtual ~CMsword2View();
#ifdef _DEBUG
    virtual void AssertValid() const;
    virtual void Dump(CDumpContext& dc) const;
#endif

    DECLARE_MESSAGE_MAP()
};

#ifndef _DEBUG
inline CMsword2Doc* CMsword2View::GetDocument() const
   { return reinterpret_cast<CMsword2Doc*>(m_pDocument); }
#endif

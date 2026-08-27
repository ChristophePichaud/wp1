#pragma once

class CFreeWordView : public CView
{
protected:
    CFreeWordView() noexcept;
    DECLARE_DYNCREATE(CFreeWordView)
private:
    CString     m_strText;      // accumulated text
    int         m_nCaretX;      // caret X position in pixels
    int         m_nCaretY;      // caret Y position in pixels
    int         m_nLineHeight;  // height of a text line
    int         m_nCharWidth;   // average character width
    CFont       m_font;         // editing font

public:
    CFeeWordDoc* GetDocument() const;
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
    virtual ~CFreeWordView();

    DECLARE_MESSAGE_MAP()
};

#ifndef _DEBUG
inline CFeeWordDoc* CFreeWordView::GetDocument() const
{
    return reinterpret_cast<CFeeWordDoc*>(m_pDocument);
}
#endif

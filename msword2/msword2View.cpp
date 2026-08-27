// msword2View.cpp : implementation of the CMsword2View class
//
// This view manages a caret and echoes keyboard input as text on screen.

#include "pch.h"
#include "framework.h"
#include "msword2.h"
#include "msword2Doc.h"
#include "msword2View.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

IMPLEMENT_DYNCREATE(CMsword2View, CView)

BEGIN_MESSAGE_MAP(CMsword2View, CView)
    ON_WM_SETFOCUS()
    ON_WM_KILLFOCUS()
    ON_WM_CHAR()
    ON_WM_KEYDOWN()
    ON_WM_SIZE()
END_MESSAGE_MAP()

// ---------------------------------------------------------------------------
// Construction / Destruction
// ---------------------------------------------------------------------------

CMsword2View::CMsword2View() noexcept
    : m_nCaretX(0)
    , m_nCaretY(0)
    , m_nLineHeight(16)
    , m_nCharWidth(8)
{
}

CMsword2View::~CMsword2View()
{
}

BOOL CMsword2View::PreCreateWindow(CREATESTRUCT& cs)
{
    return CView::PreCreateWindow(cs);
}

// ---------------------------------------------------------------------------
// OnInitialUpdate – create font and set initial caret position
// ---------------------------------------------------------------------------

void CMsword2View::OnInitialUpdate()
{
    CView::OnInitialUpdate();

    // Create a fixed-pitch font for the editing area
    m_font.CreateFont(
        20,                        // nHeight
        0,                         // nWidth
        0,                         // nEscapement
        0,                         // nOrientation
        FW_NORMAL,                 // nWeight
        FALSE,                     // bItalic
        FALSE,                     // bUnderline
        0,                         // cStrikeOut
        ANSI_CHARSET,              // nCharSet
        OUT_DEFAULT_PRECIS,        // nOutPrecision
        CLIP_DEFAULT_PRECIS,       // nClipPrecision
        CLEARTYPE_QUALITY,         // nQuality
        FIXED_PITCH | FF_MODERN,   // nPitchAndFamily
        _T("Courier New"));        // lpszFacename

    // Measure the font using a temporary DC
    CClientDC dc(this);
    RecalcMetrics(&dc);

    m_nCaretX = 0;
    m_nCaretY = 0;
}

// ---------------------------------------------------------------------------
// RecalcMetrics – measure character dimensions with current font
// ---------------------------------------------------------------------------

void CMsword2View::RecalcMetrics(CDC* pDC)
{
    CFont* pOldFont = pDC->SelectObject(&m_font);

    TEXTMETRIC tm{};
    pDC->GetTextMetrics(&tm);
    m_nLineHeight = tm.tmHeight + tm.tmExternalLeading;
    m_nCharWidth  = tm.tmAveCharWidth;

    pDC->SelectObject(pOldFont);
}

// ---------------------------------------------------------------------------
// OnDraw – render all accumulated text
// ---------------------------------------------------------------------------

void CMsword2View::OnDraw(CDC* pDC)
{
    CFont* pOldFont = pDC->SelectObject(&m_font);
    pDC->SetBkMode(OPAQUE);
    pDC->SetBkColor(RGB(255, 255, 255));
    pDC->SetTextColor(RGB(0, 0, 0));

    // Clear background
    CRect rcClient;
    GetClientRect(&rcClient);
    pDC->FillSolidRect(rcClient, RGB(255, 255, 255));

    // Draw each line of text
    int y = 0;
    int lineStart = 0;
    const int len = m_strText.GetLength();
    for (int i = 0; i <= len; ++i)
    {
        if (i == len || m_strText[i] == _T('\n'))
        {
            int lineLen = i - lineStart;
            if (lineLen > 0)
                pDC->TextOut(0, y, m_strText.Mid(lineStart, lineLen));
            y += m_nLineHeight;
            lineStart = i + 1;
        }
    }

    pDC->SelectObject(pOldFont);
}

// ---------------------------------------------------------------------------
// Caret management
// ---------------------------------------------------------------------------

void CMsword2View::UpdateCaretPos()
{
    SetCaretPos(CPoint(m_nCaretX * m_nCharWidth, m_nCaretY * m_nLineHeight));
}

void CMsword2View::OnSetFocus(CWnd* pOldWnd)
{
    CView::OnSetFocus(pOldWnd);

    // Create a caret that is 2 pixels wide and font-height tall
    CreateSolidCaret(2, m_nLineHeight);
    UpdateCaretPos();
    ShowCaret();
}

void CMsword2View::OnKillFocus(CWnd* pNewWnd)
{
    CView::OnKillFocus(pNewWnd);
    HideCaret();
    DestroyCaret();
}

void CMsword2View::OnSize(UINT nType, int cx, int cy)
{
    CView::OnSize(nType, cx, cy);
    // Nothing special needed; caret position is logical
}

// ---------------------------------------------------------------------------
// Keyboard handling
// ---------------------------------------------------------------------------

void CMsword2View::OnChar(UINT nChar, UINT nRepCnt, UINT nFlags)
{
    // Printable characters
    if (nChar >= 0x20 && nChar != 0x7F) // printable, not DEL
    {
        // Insert character at current logical position
        // Build line-based position
        int insertPos = 0;
        int curLine   = 0;
        int lineChar  = 0;
        const int len = m_strText.GetLength();
        for (int i = 0; i < len; ++i)
        {
            if (curLine == m_nCaretY && lineChar == m_nCaretX)
            {
                insertPos = i;
                goto found;
            }
            if (m_strText[i] == _T('\n'))
            {
                ++curLine;
                lineChar = 0;
            }
            else
            {
                ++lineChar;
            }
        }
        insertPos = len; // append at end

    found:
        CString ch;
        ch = static_cast<TCHAR>(nChar);
        m_strText.Insert(insertPos, ch);
        ++m_nCaretX;

        HideCaret();
        Invalidate(FALSE);
        UpdateWindow();
        UpdateCaretPos();
        ShowCaret();
    }

    CView::OnChar(nChar, nRepCnt, nFlags);
}

void CMsword2View::OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags)
{
    switch (nChar)
    {
    case VK_RETURN:
    {
        // Insert newline
        int insertPos = 0;
        int curLine   = 0;
        int lineChar  = 0;
        const int len = m_strText.GetLength();
        for (int i = 0; i < len; ++i)
        {
            if (curLine == m_nCaretY && lineChar == m_nCaretX)
            {
                insertPos = i;
                goto done_return;
            }
            if (m_strText[i] == _T('\n'))
            {
                ++curLine;
                lineChar = 0;
            }
            else
            {
                ++lineChar;
            }
        }
        insertPos = len;

    done_return:
        m_strText.Insert(insertPos, _T('\n'));
        ++m_nCaretY;
        m_nCaretX = 0;
        break;
    }

    case VK_BACK:
    {
        if (m_nCaretX > 0)
        {
            // Delete char before caret on same line
            int delPos = 0;
            int curLine = 0;
            int lineChar = 0;
            const int len = m_strText.GetLength();
            for (int i = 0; i < len; ++i)
            {
                if (curLine == m_nCaretY && lineChar == m_nCaretX)
                {
                    delPos = i - 1;
                    goto done_back;
                }
                if (m_strText[i] == _T('\n'))
                {
                    ++curLine;
                    lineChar = 0;
                }
                else
                {
                    ++lineChar;
                }
            }
            delPos = m_strText.GetLength() - 1;

        done_back:
            if (delPos >= 0)
            {
                m_strText.Delete(delPos, 1);
                --m_nCaretX;
            }
        }
        else if (m_nCaretY > 0)
        {
            // Join with previous line – delete the preceding newline
            // Find the newline ending the previous line
            int nlPos = 0;
            int curLine = 0;
            const int len = m_strText.GetLength();
            for (int i = 0; i < len; ++i)
            {
                if (m_strText[i] == _T('\n'))
                {
                    ++curLine;
                    if (curLine == m_nCaretY)
                    {
                        nlPos = i;
                        break;
                    }
                }
            }
            // Measure previous line length
            int prevLen = 0;
            for (int i = nlPos - 1; i >= 0 && m_strText[i] != _T('\n'); --i)
                ++prevLen;

            m_strText.Delete(nlPos, 1);
            --m_nCaretY;
            m_nCaretX = prevLen;
        }
        break;
    }

    case VK_LEFT:
        if (m_nCaretX > 0)
            --m_nCaretX;
        break;

    case VK_RIGHT:
    {
        // Count length of current line
        int curLen = 0;
        int curLine = 0;
        for (int i = 0; i < m_strText.GetLength(); ++i)
        {
            if (m_strText[i] == _T('\n'))
            {
                if (curLine == m_nCaretY)
                    break;
                ++curLine;
            }
            else if (curLine == m_nCaretY)
            {
                ++curLen;
            }
        }
        if (m_nCaretX < curLen)
            ++m_nCaretX;
        break;
    }

    case VK_UP:
        if (m_nCaretY > 0)
            --m_nCaretY;
        break;

    case VK_DOWN:
        ++m_nCaretY;
        break;

    case VK_HOME:
        m_nCaretX = 0;
        break;

    case VK_END:
    {
        int curLen = 0;
        int curLine = 0;
        for (int i = 0; i < m_strText.GetLength(); ++i)
        {
            if (m_strText[i] == _T('\n'))
            {
                if (curLine == m_nCaretY)
                    break;
                ++curLine;
            }
            else if (curLine == m_nCaretY)
            {
                ++curLen;
            }
        }
        m_nCaretX = curLen;
        break;
    }

    default:
        break;
    }

    HideCaret();
    Invalidate(FALSE);
    UpdateWindow();
    UpdateCaretPos();
    ShowCaret();

    CView::OnKeyDown(nChar, nRepCnt, nFlags);
}

// ---------------------------------------------------------------------------
// Debug support
// ---------------------------------------------------------------------------

#ifdef _DEBUG
void CMsword2View::AssertValid() const
{
    CView::AssertValid();
}

void CMsword2View::Dump(CDumpContext& dc) const
{
    CView::Dump(dc);
}

CMsword2Doc* CMsword2View::GetDocument() const
{
    ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CMsword2Doc)));
    return (CMsword2Doc*)m_pDocument;
}
#endif

// msword2Doc.cpp : implementation of the CMsword2Doc class
#include "pch.h"
#include "framework.h"
#include "msword2.h"
#include "msword2Doc.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

IMPLEMENT_DYNCREATE(CMsword2Doc, CDocument)

BEGIN_MESSAGE_MAP(CMsword2Doc, CDocument)
END_MESSAGE_MAP()

CMsword2Doc::CMsword2Doc() noexcept
{
}

CMsword2Doc::~CMsword2Doc()
{
}

BOOL CMsword2Doc::OnNewDocument()
{
    if (!CDocument::OnNewDocument())
        return FALSE;
    return TRUE;
}

void CMsword2Doc::Serialize(CArchive& ar)
{
    if (ar.IsStoring())
    {
    }
    else
    {
    }
}

#ifdef _DEBUG
void CMsword2Doc::AssertValid() const
{
    CDocument::AssertValid();
}

void CMsword2Doc::Dump(CDumpContext& dc) const
{
    CDocument::Dump(dc);
}
#endif

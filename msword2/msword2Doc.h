// msword2Doc.h : interface of the CMsword2Doc class
#pragma once

class CMsword2Doc : public CDocument
{
protected:
    CMsword2Doc() noexcept;
    DECLARE_DYNCREATE(CMsword2Doc)

public:
    virtual BOOL OnNewDocument();
    virtual void Serialize(CArchive& ar);

#ifdef SHARED_HANDLERS
    virtual void InitializeSearchContent();
    virtual void OnDrawThumbnail(CDC& dc, LPRECT lprcBounds);
#endif

public:
    virtual ~CMsword2Doc();
#ifdef _DEBUG
    virtual void AssertValid() const;
    virtual void Dump(CDumpContext& dc) const;
#endif

protected:
    DECLARE_MESSAGE_MAP()
};

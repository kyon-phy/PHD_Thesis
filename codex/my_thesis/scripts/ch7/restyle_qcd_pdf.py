"""Move existing label pixels with PDF clipping; never decode/re-encode images."""
from pathlib import Path
import hashlib, json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, ArrayObject

root=Path(__file__).resolve().parents[2]
source=Path('/Users/zang/Desktop/ICEPP/博士课题/leptoquark/internal_notes/ANA_EXOT_2025_06_INT1/figures/appendix/QCDCleaningCut')
# Pixel coordinates in the original embedded image: erase label area, copy
# sqrt(s) and following descriptive line, translate upwards by one line.
regions={
    'DPhi_signal': ((452,64,735,166),(452,96,735,166),34),
    'DPhi_multijets': ((122,47,402,148),(122,81,402,148),34),
    'rejection_scan': ((340,350,624,418),(340,385,624,418),35),
}
records=[]
for name,(erase,copy,shift) in regions.items():
    r=PdfReader(source/(name+'.pdf'))
    w=PdfWriter();w.add_page(r.pages[0]);page=w.pages[0]
    width,height=float(page.mediabox.width),float(page.mediabox.height)
    im=page['/Resources']['/XObject']['/Im1'].get_object()
    raw_hash=hashlib.sha256(im._data).hexdigest()
    def rect(box,dy=0):
        x0,y0,x1,y1=box
        return f'{x0/2:g} {height-y1/2+dy:g} {(x1-x0)/2:g} {(y1-y0)/2:g}'
    overlay=DecodedStreamObject()
    overlay.set_data((f'q 1 1 1 rg {rect(erase)} re f Q\n'
        f'q {rect(copy,shift/2)} re W n {width:g} 0 0 {height:g} 0 {shift/2:g} cm /Im1 Do Q\n').encode())
    previous=page.raw_get('/Contents')
    page[NameObject('/Contents')]=ArrayObject([previous,w._add_object(overlay)])
    target=root/'Figs/CH7/QCD'/f'{name}.pdf'
    w.write(target)
    check=PdfReader(target).pages[0]['/Resources']['/XObject']['/Im1'].get_object()
    assert hashlib.sha256(check._data).hexdigest()==raw_hash
    records.append(dict(source=str(source/(name+'.pdf')),target=str(target),
                        image_sha256=raw_hash,embedded_image_unchanged=True,
                        erased_label_rectangle_pixels=erase,
                        copied_label_rectangle_pixels=copy,vertical_shift_pixels=shift))
(root/'output/ch7/qcd_figure_manifest.json').write_text(json.dumps(records,indent=2))
print('Restyled three QCD labels; original embedded image bytes are unchanged.')

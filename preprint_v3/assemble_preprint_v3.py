"""Build a bilingual v2 package without refitting scientific analyses.

Source Word files supply the title, authors and unchanged scientific content.
The English title is authoritative. Filled Chinese author fields replace English
placeholders only; differing filled author fields raise an error.
"""
import argparse,copy,hashlib,json,re,shutil
from pathlib import Path
from zipfile import ZipFile
from docx import Document
from docx.shared import Inches,Pt
from docx.oxml.ns import qn

LEGENDS={
'en': 'Figure 1. Pan-cancer tissue coverage and cellular identities. (a) The harmonised atlas contains 4,720,931 cells from 72 sources and 28 cancer labels, grouped by tissue or disease category. The anatomy is schematic. (b,c) The same 1,974,309 resolved TME reference cells from 70 sources and 27 cancer labels, shown on the frozen global UMAP by eight major compartments (b) and 44 identities (c). Numbers match Table S3 and the companion key; all cells are shown. (d) Native RNA marker support: dot area indicates the RNA-positive fraction among eligible cells; colour indicates the per-gene scaled mean log1p expression after full-library normalisation to 10,000 counts. Identity means are weighted by eligible-cell counts, retaining zeros. Coverage and UMAP use the separately defined resources in Table 1.',
'zh':'图1 泛癌组织覆盖与细胞身份。（a）统一处理的图谱包含72个来源、28个癌种标签及4,720,931个细胞，按组织或疾病类别展示；人体解剖为示意。（b、c）同一组来自70个来源、27个癌种标签的1,974,309个TME参考细胞，在冻结的全局UMAP上分别按8个大类（b）及44种身份（c）着色。编号与表S3及身份对照图一致，展示全部细胞。（d）原生RNA marker支持：点面积为合格细胞中的RNA阳性比例；颜色为全库归一化至10,000计数、log1p转换后的平均表达，按基因缩放。按合格细胞数加权汇总身份均值，分母保留零表达细胞。组织覆盖与UMAP分别采用表1所定义的不同资源。'}

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def replace_text(p,text,size=None,line=None):
    rp=copy.deepcopy(p.runs[0]._r.rPr) if p.runs else None
    p.clear();r=p.add_run(text)
    if rp is not None:r._r.insert(0,rp)
    if size:r.font.size=Pt(size)
    if line:p.paragraph_format.line_spacing=Pt(line)

def author_value(text):return re.split(r'[:：]',text,maxsplit=1)[-1].strip()

def main(a):
    out=a.output;out.mkdir(parents=True,exist_ok=False)
    for n in ['manuscript','figures','supplementary_tables','figure_source_data','code','release_notes']:(out/n).mkdir()
    en=Document(a.source_en);zh=Document(a.source_zh)
    assert len(en.paragraphs)==len(zh.paragraphs)==159
    title=en.paragraphs[0].text
    # Exact translation of the supplied English title, without changing its scope.
    ztitle='泛癌单细胞图谱揭示肿瘤微环境中的细胞模块及耗竭CD8⁺ T细胞耦联'
    expected='Pan-cancer single-cell atlas defines cellular modules and exhausted CD8⁺ T-cell coupling in tumour microenvironments'
    assert title==expected,'Review the Chinese title translation for a changed English title'
    authors=[]
    for i in [2,3]:
        ev=author_value(en.paragraphs[i].text);zv=author_value(zh.paragraphs[i].text)
        if '[AUTHOR CHECK]' in ev and '[AUTHOR CHECK]' not in zv:ev=zv
        elif '[AUTHOR CHECK]' not in ev and '[AUTHOR CHECK]' not in zv:assert ev==zv,'Author discrepancy requires explicit resolution'
        authors.append(ev)
    inputs={str(p):sha(p) for p in [a.source_en,a.source_zh]}
    for lang,d in [('en',en),('zh',zh)]:
        if lang=='zh':replace_text(d.paragraphs[0],ztitle,19,26)
        for i,label in [(2,'Authors: ' if lang=='en' else '作者：'),(3,'Correspondence: ' if lang=='en' else '通讯作者：')]:
            replace_text(d.paragraphs[i],label+authors[i-2])
        text=(
         'The harmonised pan-cancer atlas spans 28 cancer labels across 72 sources (Fig. 1a). Its resolved TME identity reference contains 1,974,309 cells in eight major compartments and 44 identities (Fig. 1b,c), with native RNA marker support (Fig. 1d). The six linked resources have separately frozen cell sets, annotations and identifiers (Table 1); their cell totals are not additive.'
         if lang=='en' else
         '统一处理的泛癌图谱覆盖72个来源及28个癌种标签（图1a）。其TME细胞身份参考集包含1,974,309个细胞，分为8个大类和44种身份（图1b、c），并提供原生RNA marker支持（图1d）。六项关联资源分别冻结其细胞集合、注释和标识符（表1），各资源的细胞总数不能相加。')
        replace_text(d.paragraphs[16],text)
        p=d.paragraphs[145];blips=p._p.findall('.//'+qn('a:blip'));assert len(blips)==1
        # Allocate a new part for the figure, retaining all other image parts exactly.
        p.clear();p.add_run().add_picture(str(a.figure_dir/'Figure1_atlas_redesigned.png'),width=Inches(6.15))
        p.paragraph_format.space_before=Pt(0);p.paragraph_format.space_after=Pt(4)
        p.paragraph_format.keep_with_next=True
        replace_text(d.paragraphs[146],LEGENDS[lang],9 if lang=='en' else 9.5,11 if lang=='en' else 13)
        d.paragraphs[146].paragraph_format.space_after=Pt(0)
        d.core_properties.title=title if lang=='en' else ztitle
        d.core_properties.author=authors[0];d.core_properties.subject='Preprint v2; bilingual aligned edition'
        target=out/'manuscript'/f'PanCancer_preprint_v2_{lang}.docx';d.save(target)
        # Verify all non-edited paragraphs and table cells against the supplied source.
        original=Document(a.source_en if lang=='en' else a.source_zh)
        changed={2,3,16,145,146}|({0} if lang=='zh' else set())
        assert all(p.text==q.text for i,(p,q) in enumerate(zip(original.paragraphs,d.paragraphs)) if i not in changed)
        assert [[c.text for row in t.rows for c in row.cells] for t in d.tables]==[[c.text for row in t.rows for c in row.cells] for t in original.tables]
        assert len(d.inline_shapes)==7
        for i in range(1,7):assert d.inline_shapes[i]._inline.graphic.graphicData.pic.blipFill.blip.embed==original.inline_shapes[i]._inline.graphic.graphicData.pic.blipFill.blip.embed
        # Readable text counterpart with figures referenced, not duplicated as embedded data.
        lines=[];fig_no=0
        for child in d.element.body:
            if child.tag==qn('w:p'):
                from docx.text.paragraph import Paragraph
                p0=Paragraph(child,d)
                if p0._p.findall('.//'+qn('a:blip')):
                    fig_no+=1
                    image=next((out/'figures').glob('NOT-YET-COPIED'),None)
                    names=['Fig1_atlas_tissue_coverage.png','Fig2_source_dependence.png','Fig3_module_discovery_audit.png','Fig4_reference_module_catalogue.png','Fig5_vascular_positive_control.png','Fig6_Tex_centred_module.png','FigS1_bulk_readouts.png']
                    lines.append(f'![Figure {fig_no}](../figures/{names[fig_no-1]})')
                elif p0.text:
                    lead='# ' if p0.style.name=='Title' else '## ' if p0.style.name=='Heading 1' else '### ' if p0.style.name.startswith('Heading') else ''
                    lines.append(lead+p0.text)
            elif child.tag==qn('w:tbl'):
                from docx.table import Table
                rows=[[c.text.replace('\n','<br>').replace('|','/') for c in r.cells] for r in Table(child,d).rows]
                lines.append('\n'.join(['| '+' | '.join(rows[0])+' |','| '+' | '.join(['---']*len(rows[0]))+' |']+['| '+' | '.join(r)+' |' for r in rows[1:]]))
        (out/'manuscript'/f'PanCancer_preprint_v2_{lang}.md').write_text('\n\n'.join(lines)+'\n')
        (out/'release_notes'/f'Figure1_legend_{lang}.txt').write_text(LEGENDS[lang]+'\n')
    for f in (a.legacy_release/'figs').iterdir():
        if f.is_file() and not f.name.startswith('Fig1_'):shutil.copy2(f,out/'figures'/f.name)
    for ext in ['png','pdf','svg']:
        shutil.copy2(a.figure_dir/f'Figure1_atlas_redesigned.{ext}',out/'figures'/f'Fig1_atlas_tissue_coverage.{ext}')
        shutil.copy2(a.figure_dir/f'Figure1_companion_identity_key.{ext}',out/'figures'/f'Fig1_identity_key.{ext}')
    for f in (a.legacy_release/'supp_tables').glob('*.tsv'):shutil.copy2(f,out/'supplementary_tables'/f.name)
    shutil.copy2(a.legacy_release/'NAME_MAP_internal_to_publication.md',out/'release_notes'/'NAME_MAP_internal_to_publication.md')
    for f in (a.figure_dir/'source_tables').iterdir():shutil.copy2(f,out/'figure_source_data'/f.name)
    shutil.copy2(a.figure_dir/'source_tables'/'Figure1c_identity_key.tsv',out/'supplementary_tables'/'Table_S3_Figure1_identity_number_key.tsv')
    for f in Path(__file__).parent.glob('*.py'):shutil.copy2(f,out/'code'/f.name)
    receipt={'input_sha256':inputs,'title_en':title,'title_zh':ztitle,'authors':authors[0],'correspondence':authors[1],
      'author_resolution':'English placeholders completed from filled Chinese fields; names preserved verbatim. No affiliations or author order inferred.',
      'unchanged':'All scientific paragraphs other than atlas introduction and Figure 1 legend; all table cells; Figure 2 through S1 image relations.',
      'updated_paragraphs':[0,2,3,16,145,146]}
    (out/'release_notes'/'editorial_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print('ASSEMBLED',out)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ['source-en','source-zh','figure-dir','legacy-release','output']:p.add_argument('--'+n,type=Path,required=True)
    main(p.parse_args())

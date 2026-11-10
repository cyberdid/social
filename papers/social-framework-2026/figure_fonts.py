"""Register CMU Serif with matplotlib: the bundled OTF (CFF) files are converted to temporary TrueType
outlines because matplotlib cannot embed and subset CFF fonts correctly in PDF output."""
from __future__ import annotations

import tempfile
from pathlib import Path

from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable
from matplotlib import font_manager

FONTS = Path(__file__).resolve().parent / "manuscript/fonts"


def _to_ttf(src: Path, dst: Path) -> None:
    font = TTFont(src)
    order = font.getGlyphOrder()
    glyph_set = font.getGlyphSet()
    glyphs = {}
    for name in order:
        pen = TTGlyphPen(glyph_set)
        glyph_set[name].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
        glyphs[name] = pen.glyph()
    glyf = newTable("glyf")
    glyf.glyphOrder = order
    glyf.glyphs = glyphs
    font["glyf"] = glyf
    font["loca"] = newTable("loca")
    del font["CFF "]
    if "VORG" in font:
        del font["VORG"]
    maxp = font["maxp"]
    maxp.tableVersion = 0x00010000
    for attr in ("maxZones",):
        setattr(maxp, attr, 1)
    for attr in ("maxTwilightPoints", "maxStorage", "maxFunctionDefs", "maxInstructionDefs", "maxStackElements",
                 "maxSizeOfInstructions", "maxComponentElements"):
        setattr(maxp, attr, 0)
    maxp.maxComponentDepth = 0
    post = font["post"]
    post.formatType = 2.0
    post.extraNames = []
    post.mapping = {}
    post.glyphOrder = order
    font["head"].glyphDataFormat = 0
    font.sfntVersion = "\000\001\000\000"
    font.save(dst)


def register_cmu_serif() -> None:
    out = Path(tempfile.mkdtemp(prefix="social-cmu-"))
    for stem in ("cmunrm", "cmunbx", "cmunti", "cmunbi"):
        dst = out / f"{stem}.ttf"
        _to_ttf(FONTS / f"{stem}.otf", dst)
        font_manager.fontManager.addfont(str(dst))

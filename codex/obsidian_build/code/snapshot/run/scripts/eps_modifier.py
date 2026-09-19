from pathlib import Path
import sys, subprocess, re

p = Path(sys.argv[1])

# # modify general data/bkg. and Events title position
for f in ([p] if p.is_file() else p.glob("*.eps")):
    s = f.read_text()
    s = s.replace("122.502 176.631", "92.502 176.631") # data/bkg. label position
    s = s.replace("128.2 1105.37", "92.502 1105.37") # Events title position
    s = s.replace("56.928 sf 0 0 m (Events / 100 GeV)","62 sf 0 0 m (Events / 100 GeV)")
    #Events title size
    # remove the "Preliminary" label (drop the whole line that draws it)
    s = re.sub(r"^.*\(Preliminary\) show.*\n?", "", s, flags=re.M)
    f.write_text(s)

# modify Res signal line width
for f in ([p] if p.is_file() else p.glob("*_Res_*.eps")):
    s = f.read_text()
    s = s.replace("black 0.741176 0.121569 0.00392157 c[  12 12 ] 0 sd 6 lw", "black 0.741176 0.121569 0.00392157 c[  12 12 ] 0 sd 10 lw") # modify signal line width
    s = s.replace("0.741176 0.121569 0.00392157 c[  12 12 ] 0 sd 1342 1464 m 57 X s black", "0.741176 0.121569 0.00392157 c[  12 12 ] 0 sd 10 lw 1342 1464 m 57 X s black") # modify signal legend line width
    s = s.replace("s black[  ] 0 sd", "s black[  ] 0 sd 6 lw") # change back data error bar width
    f.write_text(s)

# modify NonRes signal line width
for f in ([p] if p.is_file() else p.glob("*_NonRes_*.eps")):
    s = f.read_text()
    s = s.replace("black 0.513726 0.176471 0.713726 c[  12 12 ] 0 sd 6 lw", "black 0.513726 0.176471 0.713726 c[  12 12 ] 0 sd 10 lw") # modify signal line width
    s = s.replace("0.513726 0.176471 0.713726 c[  12 12 ] 0 sd 1342 1464 m 57 X s black", "0.513726 0.176471 0.713726 c[  12 12 ] 0 sd 10 lw 1342 1464 m 57 X s black") # modify signal legend line width
    s = s.replace("s black[  ] 0 sd", "s black[  ] 0 sd 6 lw") # change back data error bar width
    f.write_text(s)

# modify InvM specific variable title size
for f in ([p] if p.is_file() else p.glob("*Mtaujet*.eps")):
    s = f.read_text()
    # x-axes title size
    # "[GeV]" size
    s = s.replace("2022.71 59.8267 t 0 r /Helvetica findfont 57.0348 sf 0 0 m ( [GeV]) show NC gr", "1962.71 59.8267 t 0 r /Helvetica findfont 85 sf 0 0 m ( [GeV]) show NC gr") 
     # InvM variable title size and position
    old_font_size = [25.6657, 37.0726, 37.0726, 57.0348]
    new_font_size = [50, 74, 74, 95]
    old_pos_x = [1979.98, 1957.19, 1940.09, 1891.66]
    new_pos_x = [1899.98, 1857.19, 1835.09, 1751.66]
    old_pos_y = [22.7911, 42.7334, 42.7334, 59.8267]
    new_pos_y = [22.7911, 42.7334, 42.7334, 59.8267]
    repls = {
    f"gsave  2268 456 0 0 C {old_pos_x[0]} {old_pos_y[0]} t 0 r /Helvetica findfont {old_font_size[0]} sf 0 0 m (had) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[0]} {new_pos_y[0]} t 0 r /Helvetica findfont {new_font_size[0]} sf 0 0 m (had) show NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[1]} {old_pos_y[1]} t 0 r /Symbol findfont {old_font_size[1]} sf 0 0 m ita (t) show gr NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[1]} {new_pos_y[1]} t 0 r /Symbol findfont {new_font_size[1]} sf 0 0 m ita (t) show gr NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[2]} {old_pos_y[2]} t 0 r /Helvetica-Oblique findfont {old_font_size[2]} sf 0 0 m (j) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[2]} {new_pos_y[2]} t 0 r /Helvetica-Oblique findfont {new_font_size[2]} sf 0 0 m (j) show NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[3]} {old_pos_y[3]} t 0 r /Helvetica-Oblique findfont {old_font_size[3]} sf 0 0 m (m) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[3]} {new_pos_y[3]} t 0 r /Helvetica-Oblique findfont {new_font_size[3]} sf 0 0 m (m) show NC gr",
    }
    for old, new in repls.items():
        s = s.replace(old, new)
    f.write_text(s)

# modify met variable title size and position
for f in ([p] if p.is_file() else p.glob("*_met_*.eps")):
    s = f.read_text()
    # x-axes title size
    # "[GeV]" size
    s = s.replace("2022.71 39.8845 t 0 r /Helvetica findfont 57.0348 sf 0 0 m ( [GeV]) show NC gr", "1962.71 39.8845 t 0 r /Helvetica findfont 85 sf 0 0 m ( [GeV]) show NC gr") 
     # InvM variable title size and position
    old_font_size = [37.0726, 37.0726, 57.0348]
    new_font_size = [70, 70, 95]
    old_pos_x = [1945.79, 1945.79, 1903.06]
    new_pos_x = [1820.79, 1820.79, 1743.06]
    old_pos_y = [68.3734, 22.7911, 39.8845]
    new_pos_y = [80.3734, 12.7911, 41.8845]
    repls = {
    f"gsave  2268 456 0 0 C {old_pos_x[0]} {old_pos_y[0]} t 0 r /Helvetica findfont {old_font_size[0]} sf 0 0 m (miss) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[0]} {new_pos_y[0]} t 0 r /Helvetica findfont {new_font_size[0]} sf 0 0 m (miss) show NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[1]} {old_pos_y[1]} t 0 r /Helvetica findfont {old_font_size[1]} sf 0 0 m (T) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[1]} {new_pos_y[1]} t 0 r /Helvetica findfont {new_font_size[1]} sf 0 0 m (T) show NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[2]} {old_pos_y[2]} t 0 r /Helvetica-Oblique findfont {old_font_size[2]} sf 0 0 m (E) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[2]} {new_pos_y[2]} t 0 r /Helvetica-Oblique findfont {new_font_size[2]} sf 0 0 m (E) show NC gr",
    }
    for old, new in repls.items():
        s = s.replace(old, new)
    f.write_text(s)

# modify mT variable title size and position
for f in ([p] if p.is_file() else p.glob("*_mT_*.eps")):
    s = f.read_text()
    # x-axes title size
     # InvM variable title size and position
    old_font_size = [57.0348, 37.0726, 57.0348]
    new_font_size = [95, 70, 95]
    old_pos_x = [2022.71, 1999.92, 1951.49]
    new_pos_x = [1922.79, 1879.79, 1793.06]
    old_pos_y = [48.4311, 31.3378, 48.4311]
    new_pos_y = [57.4311, 21.3378, 57.4311]
    repls = {
    f"gsave  2268 456 0 0 C {old_pos_x[0]} {old_pos_y[0]} t 0 r /Helvetica findfont {old_font_size[0]} sf 0 0 m ( [GeV]) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[0]} {new_pos_y[0]} t 0 r /Helvetica findfont {new_font_size[0]} sf 0 0 m ( [GeV]) show NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[1]} {old_pos_y[1]} t 0 r /Helvetica findfont {old_font_size[1]} sf 0 0 m (T) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[1]} {new_pos_y[1]} t 0 r /Helvetica findfont {new_font_size[1]} sf 0 0 m (T) show NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[2]} {old_pos_y[2]} t 0 r /Helvetica-Oblique findfont {old_font_size[2]} sf 0 0 m (m) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[2]} {new_pos_y[2]} t 0 r /Helvetica-Oblique findfont {new_font_size[2]} sf 0 0 m (m) show NC gr",
    }
    for old, new in repls.items():
        s = s.replace(old, new)
    f.write_text(s)

# modify mbtau variable title size and position
for f in ([p] if p.is_file() else p.glob("*InvM_N_minus_1*.eps")):
    s = f.read_text()
    # x-axes title size
     # InvM variable title size and position
    old_font_size = [57.0348, 25.6657, 37.0726, 37.0726, 57.0348]
    new_font_size = [90, 48, 70, 70, 95]
    old_pos_x = [2022.71, 1979.98, 1957.19, 1937.25, 1888.81]
    new_pos_x = [1932.71, 1859.98, 1827.19, 1787.25, 1708.81]
    old_pos_y = [56.9778, 25.64, 39.8845, 39.8845, 56.9778]
    new_pos_y = [60.9778, 20.64, 34.8845, 34.8845, 60.9778]
    repls = {
    f"gsave  2268 456 0 0 C {old_pos_x[0]} {old_pos_y[0]} t 0 r /Helvetica findfont {old_font_size[0]} sf 0 0 m ( [GeV]) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[0]} {new_pos_y[0]} t 0 r /Helvetica findfont {new_font_size[0]} sf 0 0 m ( [GeV]) show NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[1]} {old_pos_y[1]} t 0 r /Helvetica findfont {old_font_size[1]} sf 0 0 m (had) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[1]} {new_pos_y[1]} t 0 r /Helvetica findfont {new_font_size[1]} sf 0 0 m (had) show NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[2]} {old_pos_y[2]} t 0 r /Symbol findfont {old_font_size[2]} sf 0 0 m ita (t) show gr NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[2]} {new_pos_y[2]} t 0 r /Symbol findfont {new_font_size[2]} sf 0 0 m ita (t) show gr NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[3]} {old_pos_y[3]} t 0 r /Helvetica-Oblique findfont {old_font_size[3]} sf 0 0 m (b) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[3]} {new_pos_y[3]} t 0 r /Helvetica-Oblique findfont {new_font_size[3]} sf 0 0 m (b) show NC gr",
    f"gsave  2268 456 0 0 C {old_pos_x[4]} {old_pos_y[4]} t 0 r /Helvetica-Oblique findfont {old_font_size[4]} sf 0 0 m (m) show NC gr":
    f"gsave  2268 456 0 0 C {new_pos_x[4]} {new_pos_y[4]} t 0 r /Helvetica-Oblique findfont {new_font_size[4]} sf 0 0 m (m) show NC gr",
    }
    for old, new in repls.items():
        s = s.replace(old, new)
    f.write_text(s)


# modify Mljet x-axis title (m_lj [GeV]) drawn glyph-by-glyph with glyphshow.
# Enlarge font sizes AND rescale x-spacing/positions so glyphs don't overlap.
for f in ([p] if p.is_file() else p.glob("*Mljet*.eps")):
    s = f.read_text()
    # (glyph, font, old_x, old_y, old_size, new_x, new_y, new_size)
    # main glyphs: 57.0348 -> 90 ; subscript glyphs: 39.9243 -> 63 (scale ~1.58)
    # spacing scaled by the same factor and whole label shifted left (start x 1926 -> 1780)
    glyphs = [
        ("/m",         "FreeSansOblique",   "1926", "48", "57.0348", "1780", "48", "90"),
        ("/j",         "FreeSansOblique",   "1983", "37", "39.9243", "1870", "31", "63"),
        ("/afii61289", "STIXGeneral-Italic","1994", "37", "39.9243", "1887", "31", "63"),
        ("/bracketleft",  "FreeSans",       "2034", "48", "57.0348", "1950", "48", "90"),
        ("/G",         "FreeSans",          "2051", "48", "57.0348", "1977", "48", "90"),
        ("/e",         "FreeSans",          "2097", "48", "57.0348", "2050", "48", "90"),
        ("/V",         "FreeSans",          "2131", "48", "57.0348", "2104", "48", "90"),
        ("/bracketright", "FreeSans",       "2171", "48", "57.0348", "2167", "48", "90"),
    ]
    for glyph, font, ox, oy, osz, nx, ny, nsz in glyphs:
        old = f"gsave  2268 456 0 0 C {ox} {oy} t 0 r /{font} findfont {osz} sf 0 0 m {glyph} glyphshow NC gr"
        new = f"gsave  2268 456 0 0 C {nx} {ny} t 0 r /{font} findfont {nsz} sf 0 0 m {glyph} glyphshow NC gr"
        s = s.replace(old, new)
    f.write_text(s)


# modify Mlb x-axis title (m_lb [GeV]) drawn glyph-by-glyph with glyphshow.
# Enlarge font sizes AND rescale x-spacing/positions so glyphs don't overlap.
for f in ([p] if p.is_file() else p.glob("*Mlb*.eps")):
    s = f.read_text()
    # (glyph, font, old_x, old_y, old_size, new_x, new_y, new_size)
    # main glyphs: 57.0348 -> 90 ; subscript glyphs: 39.9243 -> 63 (scale ~1.58)
    # spacing scaled by the same factor and whole label shifted left (start x 1920 -> 1775)
    glyphs = [
        ("/m",         "FreeSansOblique",   "1920", "46", "57.0348", "1775", "46", "90"),
        ("/b",         "FreeSansOblique",   "1969", "34", "39.9243", "1852", "27", "63"),
        ("/afii61289", "STIXGeneral-Italic","1991", "34", "39.9243", "1887", "27", "63"),
        ("/bracketleft",  "FreeSans",       "2034", "46", "57.0348", "1955", "46", "90"),
        ("/G",         "FreeSans",          "2048", "46", "57.0348", "1977", "46", "90"),
        ("/e",         "FreeSans",          "2097", "46", "57.0348", "2054", "46", "90"),
        ("/V",         "FreeSans",          "2128", "46", "57.0348", "2103", "46", "90"),
        ("/bracketright", "FreeSans",       "2168", "46", "57.0348", "2166", "46", "90"),
    ]
    for glyph, font, ox, oy, osz, nx, ny, nsz in glyphs:
        old = f"gsave  2268 456 0 0 C {ox} {oy} t 0 r /{font} findfont {osz} sf 0 0 m {glyph} glyphshow NC gr"
        new = f"gsave  2268 456 0 0 C {nx} {ny} t 0 r /{font} findfont {nsz} sf 0 0 m {glyph} glyphshow NC gr"
        s = s.replace(old, new)
    f.write_text(s)


# add a red arrow (vertical line + right-pointing head) marking a CR/SR boundary.
arrow_x_by_name = {
    "WCR_0tau1l0b_Res_InvM_N_minus_1_Mljet_postFit": 1210,  # 800 GeV
    "topVR_1tau0l2b_Res_InvM_N_minus_1_Mtaub_postFit": 656, 
    "topCR_1tau1l_NonRes_met_N_minus_1_met_postFit": 370, # 100 GeV
    "WCR_0tau1l0b_Res_InvM_N_minus_1_Mljet_postFit": 1210,
    "WCR_0tau1l0b_NonRes_met_N_minus_1_met_postFit": 538, # 400 GeV
    "VR_0tau1l1b_Res_InvM_N_minus_1_Mlb_postFit": 1210,
    "VR_0tau1l1b_NonRes_met_N_minus_1_met_postFit": 538, # 400 GeV
    "SR_1tau0l1b_Res_InvM_N_minus_1_InvM_postFit": 1210,
    "SR_1tau0l1b_NonRes_met_N_minus_1_met_postFit": 538,
    "SR_1tau0l0b_Res_InvM_N_minus_1_Mtaujet_postFit": 1210,
    "SR_1tau0l0b_NonRes_met_N_minus_1_met_postFit": 538,
    "WCR_0tau1l0b_Res_InvM_N_minus_1_Mljet_postFit": 1210,
}
arrow_y_bottom = 449   # 10^-1 level
arrow_y_top = 1190
arrow_y_horizontal = arrow_y_top - 5 # horizontal offset
arrow_marker = "% --- CR arrow (added by eps_modifier) ---"
for f in ([p] if p.is_file() else p.glob("*.eps")):
    x = next((xv for key, xv in arrow_x_by_name.items() if key in f.name), None)
    if x is None:
        continue
    s = f.read_text()
    if arrow_marker in s:  # avoid inserting twice on re-runs
        continue
    arrow = (
        "gsave\n"
        f"{arrow_marker}\n"
        "1 0 0 c 10 lw [] 0 sd\n"
        f"newpath {x} {arrow_y_bottom} m {x} {arrow_y_top} l s\n"
        f"newpath {x - 3} {arrow_y_horizontal} m {x + 120} {arrow_y_horizontal} l s\n"
        f"newpath {x + 160} {arrow_y_horizontal} m {x + 110} {arrow_y_horizontal + 22} l {x + 110} {arrow_y_horizontal - 22} l cl f\n"
        "gr\n"
    )
    s = s.replace("gr  gr showpage", arrow + "gr  gr showpage")
    f.write_text(s)


# convert eps to pdf
for f in ([p] if p.is_file() else p.glob("*.eps")):
    pdf = f.with_suffix(".pdf")
    subprocess.run(["ps2pdf", "-dEPSCrop", str(f), str(pdf)], check=True)
    print(f"done: {f} -> {pdf}")
    
# # convert pdf to png
# for f in ([p] if p.is_file() else p.glob("*.pdf")):
#     png = f.with_suffix(".png")
#     subprocess.run(["convert", "-density", "300", str(f), str(png)], check=True)
#     print(f"done: {f} -> {png}")
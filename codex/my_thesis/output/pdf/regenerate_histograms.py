"""Regenerate the two loose-SR figures from full-precision TRExFitter exports.

No smoothing, rebinning, normalisation, or bin-width division is applied.
Only the visible signal trace is floored at the existing logarithmic frame,
as in the input ROOT plots. The exported numerical values are untouched.
Run with Python and numpy, matplotlib, PyYAML, and PyMuPDF installed.
"""
from pathlib import Path
import hashlib
import json
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import AutoMinorLocator, LogLocator, NullFormatter
from matplotlib.transforms import Bbox, offset_copy
import numpy as np
import yaml

OUT = Path(__file__).resolve().parent
FIT = Path("/Users/zang/Desktop/fit_results")
PAPER = Path("/Users/zang/Desktop/ICEPP/博士课题/leptoquark/Thesis/codex/references/ATL-COM-PHYS-2026-015.pdf")

# Match the tau-nu-b paper for ttbar, single top, diboson and the dominant
# W/Z components. Keep the separately displayed decay channels, with remaining
# colours from the ATLAS MPL/Petroff palette.
# https://atlas-mpl.readthedocs.io/en/latest/colors.html
COLOURS = {
    "ttbar": "#3f90da",
    "SingleTop": "#b9ac70",
    "Zll+j": "#832db5",
    "Z#nu#nu+j": "#94a4a2",
    "Z#tau#tau+j": "#e76300",
    "We#nu+j": "#707480",
    "Wmu#nu+j": "#92dadd",
    "W#tau#nu+j": "#ffccff",
    "Diboson": "#ffa90e",
}
LABELS = {
    "ttbar": r"$t\bar{t}$", "SingleTop": r"single $t$", "Zll+j": "Zll+j",
    "Z#nu#nu+j": r"$Z\nu\nu$+j", "Z#tau#tau+j": r"$Z\tau\tau$+j",
    "We#nu+j": r"$We\nu$+j", "Wmu#nu+j": r"$W\mu\nu$+j",
    "W#tau#nu+j": r"$W\tau\nu$+j", "Diboson": "Diboson",
}
JOBS = [
    dict(stem="loose_nonresonance_met", parameter="MU2500_gU2_5_23L1_0",
         suffix="tch_met_N_minus_1_met", region="Loose Non-Resonance SR",
         signal_label=r"$U_1$ (2.5 TeV)", xlabel=r"$E_{\mathrm{T}}^{\mathrm{miss}}$ [GeV]",
         cut=400., arrow_y=7.4),
    dict(stem="loose_resonance_mbtau", parameter="MU1500_gU1_5_23L0_6",
         suffix="sch_InvM_N_minus_1_InvM", region="Loose Resonance SR",
         signal_label=r"$U_1$ (1.5 TeV)", xlabel=r"$m_{b\tau_{\mathrm{had}}}$ [GeV]",
         cut=800., arrow_y=4.3),
]

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "DejaVu Sans"],
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial:bold",
    "font.size": 14, "axes.linewidth": .85,
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "hatch.linewidth": .38,
})


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make(job):
    directory = FIT / ("fit_taunub_nom_1l_allVR_BONLY_" + job["parameter"] +
                       "_alldecay_corrected_N_minus_1") / "Plots"
    source = directory / ("SR_1tau0l1b_loose_" + job["suffix"] + "_prefit.yaml")
    data = yaml.safe_load(source.read_text())
    original_hash = sha(source)
    edges = np.array(data["Figure"][0]["BinEdges"], dtype=float)
    samples = {s["Name"]: np.array(s["Yield"], dtype=float) for s in data["Samples"]}
    signal = samples[job["parameter"]]
    total = np.array(data["Total"][0]["Yield"], dtype=float)
    up = np.array(data["Total"][0]["UncertaintyUp"], dtype=float)
    down = np.array(data["Total"][0]["UncertaintyDown"], dtype=float)
    original_arrays = {k: v.copy() for k, v in samples.items()}
    original_total = (total.copy(), up.copy(), down.copy())
    assert np.array_equal(edges, np.arange(0, 1601, 200))
    order = [s["Name"] for s in data["Samples"][1:]][::-1]
    np.testing.assert_allclose(sum(samples[k] for k in order), total, rtol=1e-13, atol=1e-14)

    fig = plt.figure(figsize=(8, 5.1))
    ax = fig.add_axes([.100, .172, .868, .792])
    ax.set_yscale("log")
    ax.set_xlim(0, 1600)
    ax.set_ylim(.1, 100)
    bottom = np.zeros(len(total))
    for key in order:
        bars = ax.bar(edges[:-1], samples[key], np.diff(edges), bottom=bottom,
                      align="edge", color=COLOURS[key], linewidth=0, zorder=1)
        # Validate the actual plotted bar heights against the source.
        np.testing.assert_allclose([b.get_height() for b in bars], samples[key],
                                   rtol=2e-13, atol=2e-15)
        bottom = bottom + samples[key]

    low, high = total + down, total + up
    ax.fill_between(edges, np.r_[low, low[-1]], np.r_[high, high[-1]],
                    step="post", facecolor="none", edgecolor="#0000ff",
                    hatch="////", linewidth=0, zorder=3)
    # Display clipping reproduces ROOT's existing lower-frame convention.
    signal_artist = ax.stairs(np.maximum(signal, .1), edges, baseline=None,
                             color="#ff0000", linewidth=1.1,
                             linestyle=(0, (2.5, 2.5)), zorder=4)
    np.testing.assert_array_equal(signal_artist.get_data().values, np.maximum(signal, .1))
    ax.plot([job["cut"], job["cut"]], [.1, job["arrow_y"]],
            color="red", linewidth=.9, zorder=5)
    ax.annotate("", (job["cut"] + 100, job["arrow_y"]),
                (job["cut"], job["arrow_y"]),
                arrowprops=dict(arrowstyle="-|>", color="red", lw=.9,
                                shrinkA=0, shrinkB=0, mutation_scale=8), zorder=5)

    ax.set_xticks(np.arange(0, 1601, 200))
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.set_yticks([.1, 1, 10, 100])
    ax.set_yticklabels([r"$10^{-1}$", "1", "10", r"$10^{2}$"])
    ax.yaxis.set_minor_locator(LogLocator(base=10, subs=np.arange(2, 10)))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(which="both", direction="in", top=True, right=True, labelsize=14)
    ax.tick_params(which="major", length=5, width=.8, pad=4)
    ax.tick_params(which="minor", length=2.5, width=.65)
    ax.set_xlabel(job["xlabel"], fontsize=16, loc="right", labelpad=8)
    ax.set_ylabel("Events", fontsize=16, loc="top", labelpad=2)

    # A shared baseline grid keeps the five lines compact and equally spaced,
    # including the line with a square root and a superscript.
    label_baseline = .944
    label_pitch_pt = 16.0
    axis_height_pt = fig.get_figheight() * 72 * ax.get_position().height
    label_artists = [ax.text(.025, label_baseline, "ATLAS", transform=ax.transAxes,
                            fontsize=13, fontweight="bold", fontstyle="italic",
                            va="baseline")]
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    atlas_right_px = label_artists[0].get_window_extent(renderer).x1
    status_x = ax.transAxes.inverted().transform(
        (atlas_right_px + 3 * fig.dpi / 72, 0))[0]
    label_artists.append(ax.text(status_x, label_baseline,
                                "Simulation work in progress", transform=ax.transAxes,
                                fontsize=12.4, va="baseline"))
    label_rows = [label_artists.copy()]
    for line, text in enumerate([r"$\sqrt{s}$ = 13 TeV, 140 fb", "Run-2",
                                 job["region"], "Pre-fit"], start=1):
        y = label_baseline - line * label_pitch_pt / axis_height_pt
        line_artist = ax.text(.025, y, text, transform=ax.transAxes,
                              fontsize=12.8, va="baseline")
        row = [line_artist]
        if line == 1:
            # Place the unit exponent explicitly; the mixed mathtext string
            # otherwise reserves excessive ascender space for this one line.
            fig.canvas.draw()
            line_right = line_artist.get_window_extent(fig.canvas.get_renderer()).x1
            exponent_x = ax.transAxes.inverted().transform((line_right, 0))[0]
            row.append(ax.text(exponent_x, y, "−1", fontsize=9, va="baseline",
                               transform=offset_copy(ax.transAxes, fig=fig, y=5,
                                                     units="points")))
        label_artists.extend(row)
        label_rows.append(row)

    signal_handle = Line2D([], [], color="red", lw=1.1, linestyle=(0, (2.5, 2.5)))
    unc_handle = Patch(facecolor="none", edgecolor="blue", hatch="////", linewidth=0)
    left = ["SingleTop", "Z#nu#nu+j", "We#nu+j", "W#tau#nu+j"]
    right = ["ttbar", "Zll+j", "Z#tau#tau+j", "Wmu#nu+j", "Diboson"]
    handles = [signal_handle] + [Patch(facecolor=COLOURS[k]) for k in left] + [unc_handle]
    names = [job["signal_label"]] + [LABELS[k] for k in left] + ["Uncertainty"]
    handles += [Patch(facecolor=COLOURS[k]) for k in right]
    names += [LABELS[k] for k in right]
    legend = ax.legend(handles, names, ncol=2, frameon=False, fontsize=13,
              loc="upper right", bbox_to_anchor=(.985, .974), borderaxespad=0,
              handlelength=1.1, handleheight=.95, handletextpad=.45,
              columnspacing=1.6, labelspacing=.27)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    legend_box = legend.get_window_extent(renderer)
    for artist in label_artists:
        assert not legend_box.overlaps(artist.get_window_extent(renderer)), \
            "The enlarged legend overlaps the upper-left labels"
    row_boxes = [Bbox.union([text.get_window_extent(renderer) for text in row])
                 for row in label_rows]
    for previous, current in zip(row_boxes, row_boxes[1:]):
        assert current.y1 <= previous.y0, \
            "The upper-left label lines overlap"
    for artist in [ax.xaxis.label, ax.yaxis.label, *ax.get_xticklabels(), *ax.get_yticklabels()]:
        box = artist.get_window_extent(renderer)
        assert box.x0 >= 0 and box.y0 >= 0 and box.x1 <= fig.bbox.x1 and box.y1 <= fig.bbox.y1, \
            "An enlarged axis label or tick label is clipped"

    for key in samples:
        np.testing.assert_array_equal(samples[key], original_arrays[key])
    for current, original in zip((total, up, down), original_total):
        np.testing.assert_array_equal(current, original)
    assert sha(source) == original_hash

    metadata = {"Title": job["region"], "Creator": "Matplotlib; original TRExFitter bin values",
                "Subject": "No rebinning, smoothing, renormalisation or bin-width division"}
    fig.savefig(OUT / (job["stem"] + ".pdf"), metadata=metadata)
    fig.savefig(OUT / (job["stem"] + ".svg"))
    fig.savefig(OUT / (job["stem"] + ".png"), dpi=600)
    fig.savefig(OUT / (job["stem"] + "_preview.png"), dpi=140)
    plt.close(fig)
    source_copy = OUT / (job["stem"] + "_source.yaml")
    shutil.copyfile(source, source_copy)
    assert sha(source_copy) == original_hash
    return {"figure": job["stem"], "source_yaml": str(source),
            "source_pdf": str(source.with_name(source.stem.replace("_prefit", "") + ".pdf")),
            "source_sha256": original_hash,
            "bin_edges": edges.tolist(), "background_total": total.tolist(),
            "signal": signal.tolist(), "uncertainty_up": up.tolist(),
            "uncertainty_down": down.tolist(), "all_source_arrays_unchanged": True,
            "all_plotted_background_heights_verified": True,
            "graphical_signal_floor": .1, "x_limits": [0, 1600],
            "y_limits": [.1, 100], "y_scale": "log", "ratio_panel": False,
            "typography": {"ticks_pt": 14, "axis_titles_pt": 16, "legend_pt": 13,
                           "atlas_pt": 13, "status_pt": 12.4, "labels_pt": 12.8,
                           "label_baseline_pitch_pt": label_pitch_pt,
                           "legend_label_overlap": False, "axis_text_clipped": False}}


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"figures": [make(job) for job in JOBS], "colours": COLOURS,
              "colour_reference_pdf": str(PAPER), "colour_reference_page": 14,
              "additional_colour_reference": "https://atlas-mpl.readthedocs.io/en/latest/colors.html"}
    (OUT / "histogram_validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print("Created two PDF, SVG and 600 dpi PNG figures. All source arrays and plotted bar heights verified.")

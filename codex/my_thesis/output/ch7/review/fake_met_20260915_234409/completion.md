# Fake MET content moved into Chapter 7

## Content

- Section 7.1.2 now explains the instrumental origin of fake MET, its alignment with an underestimated jet, and the roles of the angular and momentum-ratio requirements.
- The two schematic panels of INT Figure C.1 are included as thesis Figure 7.1. The copied PDF files are byte-identical to their sources and contain no data points.
- Appendix B retains the loose study selection, two-dimensional distributions, threshold scan, signal retention and residual-background checks. Its repeated mechanism section was removed.
- The significance formulas, selection equations and all tabular contents are unchanged.

## Added figure commands

    \begin{figure}[htbp]
        \centering
        \begin{subfigure}{0.34\linewidth}
            \includegraphics[width=\linewidth]{Figs/CH7/QCD/fake_met_signal.pdf}
            \caption{Signal.}
        \end{subfigure}\hspace{0.08\linewidth}
        \begin{subfigure}{0.34\linewidth}
            \includegraphics[width=\linewidth]{Figs/CH7/QCD/fake_met_multijets.pdf}
            \caption{Multijet background.}
        \end{subfigure}
        \caption[Missing momentum in signal and multijet events]{Schematic transverse-plane configurations illustrating (a) genuine missing momentum from neutrinos in signal events and (b) fake missing momentum from a jet-energy mismeasurement in multijet events. Underestimating a jet momentum produces an imbalance approximately aligned with that jet, giving a small minimum jet--$\mpt$ azimuthal separation.}
        \label{fig:ch7_fake_met}
    \end{figure}

- figure[htbp] permits placement here, at the top/bottom, or on a float page. The rendered figure stays within the multijet discussion on page 3.
- \centering centres the paired panels.
- Each subfigure occupies 34% of the surrounding line width. Its \includegraphics[width=\linewidth] scales the original PDF proportionally to that panel's width.
- \hspace{0.08\linewidth} leaves an 8%-of-line-width horizontal gap between panels.
- The two inner \caption commands generate the (a)/(b) panel descriptions; the outer caption supplies the complete explanation and a shorter list-of-figures title.
- \label{fig:ch7_fake_met} together with the new Figure~\ref{fig:ch7_fake_met} creates the numbered cross-reference. Adding this figure shifts the subsequent Chapter 7 figure numbers automatically.

## Removed appendix commands

    \section{Origin of the discriminating variables}
    \label{sec:app_qcd_variables}

Removing the duplicate section removes its heading and anchor. The remaining appendix sections become B.1--B.3 automatically. No references to the removed label remain in the chapter/appendix sources.

## Validation

- Compiled with the existing MacTeX/latexmk preview command.
- Checked rendered pages 2--4 and 14--16, including the new diagram, its caption, the single-line selection formulas and all reorganised appendix pages.
- The updated preview has 18 pages and is published at output/pdf/CH7_draft.pdf.
- No undefined references/citations or overfull boxes were found. Existing class, bibliography-option, header, PDF-bookmark and TikZ-Feynman warnings remain.
- Full text changes are recorded in CH7_fake_met.diff beside this report.

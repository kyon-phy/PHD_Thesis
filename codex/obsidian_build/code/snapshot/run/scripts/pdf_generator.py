import ROOT
import argparse

def generate_histogram_pdf(input_root_file, output_pdf_file):
    """
    将ROOT文件中所有TDirectoryFile的TH1D整合到一个PDF文件中,并且以TH1D的顺序输出。

    Args:
        input_root_file (str): 输入的ROOT文件路径。
        output_pdf_file (str): 输出的PDF文件路径。
    """
    # 打开ROOT文件
    file = ROOT.TFile.Open(input_root_file)

    # 获取所有TDirectoryFile的名字
    dir_keys = [key.GetName() for key in file.GetListOfKeys() if key.GetClassName() == "TDirectoryFile"]
    if not dir_keys:
        print("No TDirectoryFile found in the ROOT file.")
        return

    # 提取NOSYS目录
    if "NOSYS" not in dir_keys:
        print("NOSYS directory not found in the ROOT file.")
        return

    # Get NOSYS TH1D list
    first_dir = file.Get("NOSYS")
    hist_keys = [key.GetName() for key in first_dir.GetListOfKeys() if key.GetClassName() == "TH1D"]

    # define which histograms to draw for each systematic
    filter_rules = {
        "GEN_*": ["met_topCR_1tau1e_tch"],
        "EG_*": ["lep_pt_0_topCR_1tau1e_tch", "met_topCR_1tau1e_tch"],
        "EL_EFF_*": ["lep_pt_0_topCR_1tau1e_tch", "met_topCR_1tau1e_tch"],
        "MUON_*": ["met_topCR_1tau1e_tch"], # will crash
        "JET_*": ["jet_pt_0_topCR_1tau1e_tch", "nJets_topCR_1tau1e_tch", "met_topCR_1tau1e_tch"],
        "FT_EFF_*": ["nbJets85_topCR_1tau1e_tch", "bjet_pt_0_topCR_1tau1e_tch", "met_topCR_1tau1e_tch"],
        "PRW_*": ["tau_pt_0_topCR_1tau1e_tch", "met_topCR_1tau1e_tch"],
        "TAUS_*": ["tau_pt_0_topCR_1tau1e_tch", "met_topCR_1tau1e_tch"],
        "MET_*": ["met_topCR_1tau1e_tch"], # will crash
    }

    # 分组逻辑：按名字相同部分分组
    grouped_dirs = {}
    for d in dir_keys:
        if d == "NOSYS":
            continue
        if "up" in d or "down" in d:
            base_name = d.rsplit("__", 1)[0]  # 去掉最后的up或down部分
        else:
            base_name = d  # 保留其他不含up或down的名字
        if base_name not in grouped_dirs:
            grouped_dirs[base_name] = []
        grouped_dirs[base_name].append(d)

    # 确保NOSYS添加到每个分组
    for group in grouped_dirs.values():
        if "NOSYS" not in group:
            group.insert(0, "NOSYS")
    # print("grouped_dirs: ", grouped_dirs)

    # 创建Latex对象
    latex = ROOT.TLatex()
    latex.SetTextSize(0.03)
    
    ########## canvas copy ##########
    # main canvas initialization
    c = ROOT.TCanvas("c", "", 800, 600)
    c.Divide(2, 2) # 2x2 canvas
    ########## canvas copy ##########
    
    # 开始写入PDF
    c.Print(output_pdf_file + "[")

    # draw histograms
    pad_counter = 0
    for group, dirs in grouped_dirs.items():
        # Check how many histograms to draw for each systematic
        for key, value in filter_rules.items():
            for dir_name in dirs:
                if key.replace("*", "") in dir_name:
                    N_hists = len(value)
                    hist_names = value
                    sys_name = key.replace("_*", "")
                    break

        for i, hist_name in enumerate(hist_keys):
            # check if the histogram is valid for the systematic
            if hist_name not in hist_names:
                continue
                        
            ########## canvas copy ##########
            # creat sub canvas
            sub_canvas_name = f"sub_canvas_{pad_counter}"
            sub_canvas = ROOT.TCanvas(sub_canvas_name, "", 800, 600)

            # go to sub canvas
            sub_canvas.cd()
            ########## canvas copy ##########
            
            # draw top sub pad
            pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
            pad1.SetBottomMargin(0)
            pad1.SetLogy(1)
            pad1.Draw()
            pad1.cd()

            legend = ROOT.TLegend(0.5, 0.7, 0.9, 0.9)
            colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta, ROOT.kCyan]
            line_styles = [1, 2, 3, 4, 5]  # 实线、虚线、点划线等
            color_index = 0

            # 遍历分组内的目录
            nosys_hist = None
            hists = []
            for dir_name in dirs:
                directory = file.Get(dir_name)
                if not directory:
                    continue

                hist = directory.Get(hist_name)
                if not hist:
                    continue

                hist.SetLineColor(colors[color_index % len(colors)])
                hist.SetLineStyle(line_styles[color_index % len(line_styles)])  # 设置线条样式
                hist.SetLineWidth(2)  # 设置线条宽度
                hist.GetYaxis().SetTitle("Events")
                hist.GetYaxis().SetTitleSize(0.07)
                hist.GetYaxis().SetTitleOffset(0.6)
                hist.GetYaxis().SetLabelSize(0.06)
                hist.SetStats(0)  # 不显示右上角统计框
                draw_option = "HIST SAME" if color_index > 0 else "HIST"
                hist.Draw(draw_option)
                legend.AddEntry(hist, dir_name, "l")
                hist_clone = hist.Clone(f"hist_clone_{dir_name}")
                hists.append(hist_clone)
                if dir_name == "NOSYS":
                    nosys_hist = hist
                color_index += 1
            
            # draw legend
            legend.Draw()
            
            # draw latex
            latex.SetTextSize(0.06)
            latex.DrawLatexNDC(0.3, 0.65, f"Sys: {group}")
            # latex.DrawLatexNDC(0.35, 0.60, f"Hist: {hist_name}")
            
            print(f"Saving histograms {hist_name} from systematic: {group}")

            ########## canvas copy ##########
            # go to sub canvas
            sub_canvas.cd()
            ########## canvas copy ##########
            # draw bottom pad
            pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
            pad2.SetTopMargin(0)
            pad2.SetBottomMargin(0.5)
            pad2.SetLogy(0)
            pad2.Draw()
            pad2.cd()

            # print("zip: ", list(zip(hists, dirs)))
            for hist, dir_name in zip(hists, dirs):
                if dir_name == "NOSYS":
                    continue
                
                # set ratio_hist format
                ratio_hist = hist
                ratio_hist.Divide(nosys_hist)  # 计算比例
                ratio_hist.SetLineColor(hist.GetLineColor())
                ratio_hist.SetLineStyle(hist.GetLineStyle())
                ratio_hist.SetLineWidth(2)
                ratio_hist.GetYaxis().SetTitle("Ratio")
                ratio_hist.GetYaxis().SetNdivisions(505)
                ratio_hist.GetYaxis().SetTitleSize(0.2)
                ratio_hist.GetYaxis().SetTitleOffset(0.5)
                ratio_hist.GetYaxis().SetLabelSize(0.15)
                ratio_hist.GetXaxis().SetTitleSize(0.2)
                ratio_hist.GetXaxis().SetTitleOffset(1.0)
                ratio_hist.GetXaxis().SetLabelSize(0.15)

                # set y axis range
                Ymax=ratio_hist.GetMaximum()
                Ymin=ratio_hist.GetMinimum()
                range_y = max(abs(Ymax-1), abs(Ymin-1))
                range_y = 0.1 if Ymax == Ymin == 1 else range_y
                range_y = 1 if range_y > 1 else range_y
                # ratio_hist.GetYaxis().SetRangeUser(1-(range_y*1.5), 1+(range_y*1.5))
                ratio_hist.GetYaxis().SetRangeUser(0.95, 1.05)
                
                # draw ratio_hist
                ratio_hist.Draw("HIST SAME")

            # 添加y=1的参考线
            line = ROOT.TLine(ratio_hist.GetXaxis().GetXmin(), 1, ratio_hist.GetXaxis().GetXmax(), 1)
            line.SetLineColor(ROOT.kRed)
            line.SetLineStyle(4)
            line.Draw("SAME")
            
            ########## canvas copy ##########
            # copy sub canvas to main canvas
            c.cd(pad_counter + 1)
            sub_canvas.DrawClonePad()
            ########## canvas copy ##########
            
            pad_counter += 1
                        
            # save current canvas while the pad_counter is 4 or the last histogram of the systematic
            if pad_counter == 4 or (pad_counter == N_hists and sys_name != "GEN" and sys_name != "MET" and sys_name != "MUON"): # add sys name in case it cause the crash
                c.Print(output_pdf_file)
                c.Clear()
                c.Divide(2, 2)
                pad_counter = 0
        # break
    # 结束PDF写入
    if pad_counter != 0:
        c.Print(output_pdf_file)
    c.Print(output_pdf_file + "]")

    print(f"All histograms are saved to {output_pdf_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate histogram PDF from ROOT file.")
    parser.add_argument("--input", type=str, help="Path to the input ROOT file.", default="output_taunub_sys_mc20e/ttbar.root")
    parser.add_argument("--output", type=str, help="Path to the output PDF file.", default="histograms_combined_ttbar_sys_mc20e.pdf")
    args = parser.parse_args()

    generate_histogram_pdf(args.input, args.output)

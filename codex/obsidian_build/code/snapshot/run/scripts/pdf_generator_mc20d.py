import ROOT

def generate_histogram_pdf(input_root_file, output_pdf_file):
    """
    将ROOT文件中所有TDirectoryFile的TH1D整合到一个PDF文件中,并且以TH1D的顺序输出。

    Args:
        input_root_file (str): 输入的ROOT文件路径。
        output_pdf_file (str): 输出的PDF文件路径。
    """
    # 打开ROOT文件
    file = ROOT.TFile.Open(input_root_file)

    # 获取第一个TDirectoryFile的名字
    dir_keys = [key.GetName() for key in file.GetListOfKeys() if key.GetClassName() == "TDirectoryFile"]
    if not dir_keys:
        print("No TDirectoryFile found in the ROOT file.")
        return

    first_dir = file.Get(dir_keys[0])  # 使用第一个TDirectoryFile

    # 获取第一个目录中的TH1D名称
    hist_keys = [key.GetName() for key in first_dir.GetListOfKeys() if key.GetClassName() == "TH1D"]

    # 创建一个PDF输出文件
    c = ROOT.TCanvas("c", "", 800, 600)

    # 开始写入PDF
    c.Print(output_pdf_file + "[")

    # 创建Latex对象
    latex = ROOT.TLatex()
    latex.SetTextSize(0.03)
    
    # 遍历TH1D名称并从所有TDirectoryFile中提取并绘制
    count = 0
    c.SetLogy()
    for hist_name in hist_keys:
        for dir_name in dir_keys:
            directory = file.Get(dir_name)  # 获取TDirectoryFile
            hist = directory.Get(hist_name)  # 获取TH1D对象

            c.Clear()
            # draw hist
            # hist.SetLineColor(ROOT.kRed)  # 设置线条颜色以区分
            hist.SetMaximum(1e6)
            hist.SetMinimum(1e-1)
            hist.Draw()  # 绘制直方图
            # draw latex
            latex.DrawLatexNDC(0.45, 0.75, f"Systematic: {dir_name}")
            latex.DrawLatexNDC(0.45, 0.70, f"Histogram: {hist_name}")
            
            print(f"Saving histograms {hist_name} from {dir_name}")
            c.Print(output_pdf_file)  # 保存当前画布到PDF
            count += 1
            if count > 1:
                count = 0
                # break 
        # break
    # 结束PDF写入
    c.Print(output_pdf_file + "]")

    print(f"All histograms are saved to {output_pdf_file}.")

# 示例调用
generate_histogram_pdf("output_taunub_sys_mc20d/ttbar.root", "histograms_combined_ttbar_sys_mc20d.pdf")

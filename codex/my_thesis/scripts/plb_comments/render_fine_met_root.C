// Reproduce the historical figure's ROOT typography without altering source bins.
// Run in an isolated directory with both downloaded ROOT files beside this macro.
#include <TArrow.h>
#include <TCanvas.h>
#include <TColor.h>
#include <TFile.h>
#include <TGraphAsymmErrors.h>
#include <TH1.h>
#include <TH1D.h>
#include <THStack.h>
#include <TLatex.h>
#include <TLegend.h>
#include <TLine.h>
#include <TMath.h>
#include <TPad.h>
#include <TStyle.h>
#include <TSystem.h>
#include <cassert>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

void render_fine_met_root(bool modified=true) {
  const std::string region="VR_0tau1l1b_tch_met_N_minus_1_met";
  TFile source("fit_taunub_N_minus_1_histos.root","READ");
  TFile plotted((region+".root").c_str(),"READ");
  auto read=[&](const std::string& sample) {
    // The nominal objects, NOT the preprocessing *_orig objects, enter the plot.
    auto key=region+"/"+sample+"/nominal/"+region+"_"+sample;
    auto h=dynamic_cast<TH1*>(source.Get(key.c_str())); assert(h);
    std::vector<double> edges;
    for(int b=1;b<=h->GetNbinsX()+1;++b)edges.push_back(h->GetBinLowEdge(b));
    auto clone=new TH1D(sample.c_str(),"",h->GetNbinsX(),edges.data());
    clone->SetDirectory(nullptr);
    for(int b=0;b<=h->GetNbinsX()+1;++b){clone->SetBinContent(b,h->GetBinContent(b));clone->SetBinError(b,h->GetBinError(b));}
    return clone;
  };
  std::vector<std::string> names={"ttbar","SingleTop","Zjets","Wjets","Diboson","Dijet"};
  std::vector<std::vector<std::string>> members={
    {"ttbar_dilep","ttZ"}, {"SingleTop_tch","SingleTop_sch","SingleTop_tW"},
    {"Zll","Znunu","Ztautau","Zjet_EWK"}, {"Wlnu","Wtaunu_METTAU","Wtaunu_HF"},
    {"Diboson","Diboson_semiLep"}, {"Dijet"}};
  std::vector<TH1*> h;
  for(unsigned i=0;i<names.size();++i) {
    auto sum=read(members[i][0]); sum->SetName(names[i].c_str());
    for(unsigned j=1;j<members[i].size();++j){auto part=read(members[i][j]);sum->Add(part);delete part;}
    h.push_back(sum);
  }
  auto data=read("Data");
  auto total=dynamic_cast<TH1*>(h[0]->Clone("total_background"));total->SetDirectory(nullptr);
  for(unsigned i=1;i<h.size();++i)total->Add(h[i]);
  auto band=dynamic_cast<TGraphAsymmErrors*>(plotted.Get(("Graph_from_"+region+"_Dijet").c_str())->Clone("plotted_uncertainty"));
  for(int b=1;b<=40;++b){assert(std::abs(total->GetBinContent(b)-band->GetY()[b-1])<1e-11);}

  gStyle->SetOptStat(0);gStyle->SetOptTitle(0);
  gStyle->SetCanvasColor(0);gStyle->SetPadColor(0);gStyle->SetFrameFillColor(0);
  gStyle->SetFrameBorderMode(0);gStyle->SetCanvasBorderMode(0);gStyle->SetPadBorderMode(0);
  // The original 1240x904 bitmap is the size reference. Helvetica pixel fonts
  // retain the original normal text, with Helvetica bold-oblique for ATLAS.
  gStyle->SetTextFont(43);gStyle->SetTextSize(30);
  for(auto axis:{"X","Y","Z"}) {
    gStyle->SetLabelFont(43,axis);gStyle->SetTitleFont(43,axis);
    gStyle->SetLabelSize(30,axis);gStyle->SetTitleSize(30,axis);
  }
  gStyle->SetEndErrorSize(0);gStyle->SetErrorX(0.5);
  gStyle->SetLineScalePS(2);
  gStyle->SetHatchesLineWidth(1);gStyle->SetHatchesSpacing(1.0);
  auto canvas=new TCanvas("fine_met","",1240,904);canvas->SetCanvasSize(1240,904);
  const double left=98./1240.,right=41./1240.;
  auto upper=new TPad("upper","",0,0.28,1,1);
  auto lower=new TPad("lower","",0,0,1,0.28);
  for(auto pad:{upper,lower}){pad->SetLeftMargin(left);pad->SetRightMargin(right);pad->SetTicks(1,1);pad->SetFillStyle(0);}
  upper->SetTopMargin(29./(904*.72));upper->SetBottomMargin(0);upper->SetLogy();
  lower->SetTopMargin(0);lower->SetBottomMargin(108./(904*.28));
  lower->Draw();upper->Draw();upper->cd();
  auto frame=dynamic_cast<TH1*>(total->Clone("frame"));frame->SetDirectory(nullptr);frame->Reset();
  frame->UseCurrentStyle();frame->SetMinimum(.1);frame->SetMaximum(1e5);
  frame->GetXaxis()->SetRangeUser(0,1000);frame->GetXaxis()->SetLabelSize(0);
  frame->GetXaxis()->SetNdivisions(510);frame->GetXaxis()->SetTickLength(.02);
  frame->GetYaxis()->SetTickLength(.01);frame->GetYaxis()->SetTitle("");
  frame->GetYaxis()->SetTitleOffset(.92);frame->GetYaxis()->SetTitleSize(30);
  frame->GetYaxis()->SetLabelSize(30);frame->Draw("AXIS");
  const int paper[]={TColor::GetColor(.24707f,.564453f,.855469f),TColor::GetColor(.724609f,.673828f,.439209f),
    TColor::GetColor(.580078f,.642578f,.634766f),TColor::GetColor(1.f,.800781f,1.f),
    TColor::GetColor(1.f,.662109f,.0549011f),TColor::GetColor("#b3a86b")};
  const int old[]={TColor::GetColor("#548fcc"),TColor::GetColor("#b43017"),TColor::GetColor("#7934ad"),
    TColor::GetColor("#747782"),TColor::GetColor("#f5af33"),TColor::GetColor("#b3a86b")};
  std::vector<TH1*> cumulative;
  for(int i=5;i>=0;--i){
    h[i]->SetFillColor(modified?paper[i]:old[i]);h[i]->SetLineColor(h[i]->GetFillColor());h[i]->SetLineWidth(1);h[i]->SetFillStyle(1001);
    auto layer=dynamic_cast<TH1*>(h[i]->Clone(Form("cumulative_%d",i)));layer->SetDirectory(nullptr);
    if(!cumulative.empty())layer->Add(cumulative.back());cumulative.push_back(layer);
  }
  // Paint cumulative histograms from the full total down to the bottom layer;
  // this is the same stack geometry, without ROOT's delayed THStack ownership.
  for(auto i=cumulative.rbegin();i!=cumulative.rend();++i)(*i)->Draw("HIST SAME");
  band->SetFillStyle(3354);band->SetFillColor(kBlue-7);band->SetLineColor(kWhite);band->SetLineWidth(0);band->SetMarkerSize(0);band->Draw("E2 SAME");
  auto points=new TGraphAsymmErrors();points->SetName("data_points");
  auto ratio=new TGraphAsymmErrors();ratio->SetName("data_ratio");
  for(auto g:{points,ratio}){g->SetMarkerStyle(20);g->SetMarkerSize(2.0);g->SetMarkerColor(1);g->SetLineColor(1);g->SetLineWidth(2);}
  for(int b=1;b<=40;++b){
    double n=data->GetBinContent(b);if(n==0)continue;
    double x=data->GetBinCenter(b),y=total->GetBinContent(b);
    // Match the original TRExPlot::poissonize tail probability.
    double lo=n-.5*TMath::ChisquareQuantile(.1586555,2*n);
    double hi=.5*TMath::ChisquareQuantile(1-.1586555,2*(n+1))-n;
    int p=points->GetN();points->SetPoint(p,x,n);points->SetPointError(p,0,0,lo,hi);
    ratio->SetPoint(p,x,n/y);ratio->SetPointError(p,0,0,lo/y,hi/y);
  }
  points->Draw("PZ SAME");
  auto text=[&](double x,double y,const char* label,int font=43,int colour=1){
    auto t=new TLatex(x,y,label);t->SetNDC();t->SetTextFont(font);t->SetTextSize(30);t->SetTextColor(colour);t->Draw();return t;
  };
  // Baselines and spacing measured from the original bitmap.
  text(136./1240.,1-91./650.88,"ATLAS",73);
  text(256./1240.,1-91./650.88,"Internal");
  text(136./1240.,1-134./650.88,"#sqrt{s} = 13 TeV, 140 fb^{-1}");
  if(modified){
    text(136./1240.,1-178./650.88,"VRW-NonRes");
    text(136./1240.,1-221./650.88,"Pre-Fit");
    auto leg=new TLegend(.565,1-239./650.88,.955,1-54./650.88);
    leg->SetNColumns(2);leg->SetBorderSize(0);leg->SetFillStyle(0);
    leg->SetTextFont(43);leg->SetTextSize(30);leg->SetMargin(.20);leg->SetColumnSeparation(.035);
    leg->AddEntry(points,"Data","lep");leg->AddEntry(h[3],"W+jets","f");
    leg->AddEntry(h[4],"Diboson","f");leg->AddEntry(h[0],"t#bar{t}","f");
    leg->AddEntry(h[1],"single t","f");leg->AddEntry(h[2],"Z+jets","f");
    leg->AddEntry(band,"Uncertainty","f");leg->Draw();
    auto vrline=new TLine(400,.1,400,1e3);vrline->SetLineColor(kRed);vrline->SetLineWidth(3);vrline->Draw();
    auto vr=new TArrow(400,1e3,490,1e3,.018,"|>");vr->SetLineColor(kRed);vr->SetFillColor(kRed);vr->SetLineWidth(3);vr->Draw();
    auto vrtext=new TLatex(420,1400,"VR");vrtext->SetTextFont(43);vrtext->SetTextSize(30);vrtext->SetTextColor(kRed);vrtext->Draw();
  }else{
    text(136./1240.,1-178./650.88,"fit_taunub_nom_1l_allVR_N_minus_1");
    text(136./1240.,1-221./650.88,"0#tau1l1b, Non-Resonance 0tauVR");
    text(136./1240.,1-264./650.88,"Pre-Fit");
    auto leg=new TLegend(.45,1-448.75/650.88,.735,1-57.25/650.88);
    leg->SetBorderSize(0);leg->SetFillStyle(0);leg->SetTextFont(43);leg->SetTextSize(30);leg->SetTextAlign(32);leg->SetMargin(.22);
    leg->AddEntry(points,"Data","lep");
    const char* labels[]={"ttbar","SingleTop","Z+jets","W+jets","Diboson","Dijet"};
    for(int i=0;i<6;++i)leg->AddEntry(h[i],labels[i],"f");
    leg->AddEntry((TObject*)nullptr,"Total","");leg->AddEntry(band,"Uncertainty","f");leg->Draw();
    std::vector<double> yields={data->Integral()};for(auto hist:h)yields.push_back(hist->Integral());yields.push_back(total->Integral());
    for(unsigned i=0;i<yields.size();++i){auto t=text(.925,1-(89+i*43.5)/650.88,Form("%.1f",yields[i]));t->SetTextAlign(31);}
  }
  upper->RedrawAxis();lower->cd();
  auto rframe=dynamic_cast<TH1*>(total->Clone("ratio_frame"));rframe->SetDirectory(nullptr);rframe->Reset();rframe->UseCurrentStyle();
  rframe->SetMinimum(0);rframe->SetMaximum(2);rframe->GetYaxis()->SetNdivisions(504);
  rframe->GetYaxis()->SetTitle("");rframe->GetYaxis()->SetTitleOffset(.92);
  rframe->GetYaxis()->SetTickLength(.01);rframe->GetYaxis()->ChangeLabel(-1,-1,-1,-1,-1,-1," ");
  rframe->GetXaxis()->SetNdivisions(510);rframe->GetXaxis()->SetLabelOffset(.025);
  rframe->GetXaxis()->SetTitle("");
  rframe->Draw("AXIS");
  auto rband=dynamic_cast<TGraphAsymmErrors*>(band->Clone("relative_uncertainty"));
  for(int i=0;i<40;++i){double y=total->GetBinContent(i+1);rband->SetPoint(i,rband->GetX()[i],1);rband->SetPointEYlow(i,y>1e-4?band->GetErrorYlow(i)/y:0);rband->SetPointEYhigh(i,y>1e-4?band->GetErrorYhigh(i)/y:0);}
  rband->Draw("E2 SAME");
  auto unity=new TLine(0,1,1000,1);unity->SetLineStyle(3);unity->SetLineWidth(2);unity->Draw();
  ratio->Draw("PZ SAME");
  for(int i=0;i<ratio->GetN();++i)if(ratio->GetY()[i]>2){
    double x=ratio->GetX()[i];auto a=new TArrow(x,1.9,x,2,.030/(1240./596.),"|>");
    a->SetFillColor(10);a->SetLineColor(kBlue-7);a->SetLineWidth(2);a->SetAngle(40);a->Draw();
  }
  lower->RedrawAxis();canvas->cd();
  // Fixed canvas positions reproduce the bitmap margins without ROOT's
  // pad-dependent title offsets clipping the large labels.
  auto title=[&](double x,double y,const char* value,double angle){
    auto t=new TLatex(x/1240.,y/904.,value);t->SetNDC();t->SetTextFont(43);t->SetTextSize(30);
    t->SetTextAlign(31);t->SetTextAngle(angle);t->Draw();
  };
  title(35,904-29,"Events",90);title(35,904-655,"Data / Bkg.",90);
  title(1199,24,modified?"E_{T}^{miss} [GeV]":"met",0);
  canvas->Update();
  std::string stem=modified?"VRW_NonRes_MET_25GeV_paper_style":"VRW_NonRes_MET_25GeV_ROOT_reconstructed";
  canvas->Print((stem+".eps").c_str());canvas->Print((stem+".png").c_str());
  TFile check((stem+"_verification.root").c_str(),"RECREATE");
  for(auto hist:h)hist->Write();data->Write();total->Write();band->Write();points->Write();ratio->Write();rband->Write();canvas->Write();check.Close();
  std::cout<<"final-bin single-top = "<<h[1]->GetBinContent(40)<<", total = "<<total->GetBinContent(40)<<std::endl;
}

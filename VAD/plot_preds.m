function [result] = plot_preds(file, threshold, output_type, winlen, winstep)

  addpath(genpath('./lib'));
  
  %% parameter setting
  
  audio_dir = file;

  %% load in posterior probabilites from matrix
  load('./result/pred.mat');

  s = audioread(audio_dir);
  
  %% posterior probabilities to binary classification
  pp = pred;
  result = zeros(length(pp), 1);
  result(pp>threshold) = 1;

  %% plotting the signal and predictions
  if output_type == 1
      result = frame2rawlabel(result, winlen, winstep);
      pp = frame2inpt(pp, winlen, winstep);
  end

  pred_figure = figure
  t = (1:length(s))./16000;
  p1 = plot(t, s);
  hold on
  p3 = plot(t(1:length(result)), result*0.15, 'r');
  ylim([-0.3 0.6]);
  xlim([0 t(end)]);
  legend([p3],'prediction')

  saveas(pred_figure,'preds.jpg')

end

library(ggplot2)
cat("\014") 
options(max.print=1000000)

t1 <- Sys.time()

# H_FILE <- "/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/navigation_mining/H_NAVI_INTERVAL.csv"
# L_FILE <- "/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/navigation_mining/L_NAVI_INTERVAL.csv"
# h_dat <- read.csv(H_FILE)   
# h_val <- h_dat$H_NAVI_INTERVAL
# 
# l_dat <- read.csv(L_FILE)   
# l_val <- l_dat$L_NAVI_INTERVAL
# y_limit <- c(0, 5)

# H_FILE <- "/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/edit_mining/median/H_NORM_EDIT_INTERVAL.csv"
# L_FILE <- "/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/edit_mining/median/L_NORM_EDIT_INTERVAL.csv"
# y_limit <- c(0, 2.5)
# h_dat <- read.csv(H_FILE)   
# h_val <- h_dat$H_NORM_EDIT_INTERVAL
# 
# l_dat <- read.csv(L_FILE)   
# l_val <- l_dat$L_NORM_EDIT_INTERVAL
# 
# h_val <- as.numeric(h_val)
# l_val <- as.numeric(l_val)

# H_FILE <- "/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/debug_mining/H_DEBUG_INTERVAL.csv"
# L_FILE <- "/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/debug_mining/L_DEBUG_INTERVAL.csv"
# y_limit <- c(0, 3.5)
# h_dat <- read.csv(H_FILE)   
# h_val <- h_dat$H_DEBUG_INTERVAL
# 
# l_dat <- read.csv(L_FILE)   
# l_val <- l_dat$L_DEBUG_INTERVAL
# 
# h_val <- as.numeric(h_val)
# l_val <- as.numeric(l_val)



doBoxPlot<- function(xLabelP, yLabelP, data2plot, limitP)
{
  box_plot <- ggplot(data2plot, aes(x=group, y=value, fill=group)) + geom_boxplot(width = 0.25, outlier.shape=16, outlier.size=1) + labs(x=xLabelP, y=yLabelP)
  box_plot<-  box_plot + theme(plot.title = element_text(hjust = 0.5), text = element_text(size=15), legend.position="none", axis.text=element_text(size=22))
  box_plot <- box_plot + scale_y_continuous(limits=limitP) 
  box_plot <- box_plot + stat_summary(fun.y=mean, geom="point", colour="darkred", shape=18, size=3) 
  box_plot
}

a <- data.frame(group = "HIGH", value = h_val)
b <- data.frame(group = "LOW",  value = l_val)
# Combine into one long data frame
dataset_plot <- rbind(a, b)
doBoxPlot('Comprehension Effort', 'Normalized Time Interval', dataset_plot, y_limit)

t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))
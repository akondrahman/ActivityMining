cat("\014") 
library(ggplot2)  
options(max.print=1000000)
t1 <- Sys.time()

sil_file <- '/Users/akond/Documents/AkondOneDrive/MSR18-MiningChallenge/output/sil.csv'

sil_data <- read.csv(sil_file)
sil_plot <- ggplot() + geom_line(aes(y = sil, x =count), data = sil_data, stat="identity")
sil_plot <- sil_plot + labs(x="Cluster Count", y="Silhouette Width") +  scale_x_continuous(breaks=seq(2, 25, 1))
sil_plot
t2 <- Sys.time()
print(t2 - t1)  
rm(list = setdiff(ls(), lsf.str()))
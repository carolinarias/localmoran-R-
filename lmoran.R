
#------------------------------------------------------------------------------------------------------------------
# MORAN INDEX

#File name: lmoran.R
#Description: This script takes the stations data coming from the weather underground API, makes some preprocessing 
#and cleanning to finally map the data with the telecom Italia Milano GRID.
#Author:Carolina Arias Munoz. Modified from: https://rpubs.com/corey_sparks/105700, http://rstudio-pubs-static.s3.amazonaws.com/4938_b5fc230d586c48b291627ff6ea484d2e.html
#Date Created: 30/07/2016
#Date Last Modified: 30/07/2016
#R version: 3.3.0 (2016-05-03)
#------------------------------------------------------------------------------------------------------------------

library(rasterVis)
library(maptools)
library(rgrass7)
library(ggplot2)
library(spdep)

#Import data
testraster<-readRAST("sms_out_mean")
milanogrid<-readShapePoly('/media/sf_2_PhD_2013_-2014/1PhD_WorkDocs/PhD_Data-calculations/spatial data/milano-grid.shp', proj4string=CRS("+proj=utm +zone=32 +north"))

#List of neighbours for a grid of cells
milanogrid.nb <- cell2nb(100, 100, type="rook", torus=TRUE)
summary(milanogrid.nb)
# Neighbour list object:
# Number of regions: 10000 
# Number of nonzero links: 40000 
# Percentage nonzero weights: 0.04 
# Average number of links: 4 

#spatial weights object
lw <- nb2listw(milanogrid.nb)

#convert raster values to vector
m <- as.matrix(testraster)
x <- as.vector(m)
# Adding raster values to milanogrid
milanogrid$values <- x

#calculating local moran statistic
lm <- localmoran(x, lw,p.adjust.method="fdr")
plot (lm)
View (lm)
summary(lm)

#Adding local moran Li result to the milano grid
milanogrid$lmi<-lm[,1]
#Adding the p value result to the milano grid 
milanogrid$lmp<-lm[,5]
#Adding the z value result to the milano grid 
milanogrid$z<-lm[,4]

# Creating the cluster identifiers
milanogrid$cl<-as.factor(ifelse(milanogrid$lmp<=.05,"Clustered","NotClustered"))

#plotting clusters
class <- classIntervals(x,10, style='jenks')
classIntervals()

spplot(milanogrid, "lmi", main="Local Moran's I", at=quantile(milanogrid$lmi), col.regions=brewer.pal(n=10, "RdBu"))
spplot(milanogrid, "lmi", main="Local Moran's I", at=class$brks, col.regions=brewer.pal(n=5, "RdBu"))
spplot(milanogrid, "cl", main="Local Moran Clusters", col.regions=c(2,0))

#moran scatterplot
mp <- moran.plot(x, lw, xlab='incoming SMS', ylab='Lagged incoming SMS', main=c('Moran Scatterplot for incoming SMS', "in Milan. I=.655"), zero.policy = TRUE, labels = TRUE)
View (mp)
summary(mp)

#lagval 
milanogrid$lagvalues<- lag.listw(lw, x)

# identify the moran plot quadrant for each observation
milanogrid$quad_sig <- NA
milanogrid@data[(milanogrid$values >= 0 & milanogrid$lagvalues >= 0) & (lm[, 5] <= 0.05), "quad_sig"] <- "high-High (cluster)"
milanogrid@data[(milanogrid$values <= 0 & milanogrid$lagvalues <= 0) & (lm[, 5] <= 0.05), "quad_sig"] <- "low-Low (cluster)"
milanogrid@data[(milanogrid$values >= 0 & milanogrid$lagvalues <= 0) & (lm[, 5] <= 0.05), "quad_sig"] <- "High-Low (outlier)"
milanogrid@data[(milanogrid$values >= 0 & milanogrid$lagvalues <= 0) & (lm[, 5] <= 0.05), "quad_sig"] <- "Low-High (outlier)"
milanogrid@data[(milanogrid$values <= 0 & milanogrid$lagvalues >= 0) & (lm[, 5] <= 0.05), "quad_sig"] <- "Not Signif." 

#Mapping the results
# Breaks for the thematic map classes
breaks <- seq(1, 5, 1)

# Labels for the thematic map classes
labels <- c("high-High (cluster)", "low-Low (cluster)", "High-Low (outlier)", "Low-High (outlier)", "Not Signif.")

# see ?findInterval - This is necessary for making a map
np <- findInterval(milanogrid$quad_sig, breaks)

# Assign colors to each map class
colors <- c("lightpink","red", "blue", "skyblue2", "white")
plot(milanogrid, col = colors[np])  #colors[np] manually sets the color for each cell
#mtext("Local Moran's I", cex = 1.5, side = 3, line = 1)
legend("topleft", legend = labels, fill = colors, bty = "n")

write.csv(milanogrid, file = '/media/sf_2_PhD_2013_-2014/4PhD_Corsi/EFFETTIVO/ADVANCED GIS/scripts/lm_smsin.csv')

citation(package = 'spdep')
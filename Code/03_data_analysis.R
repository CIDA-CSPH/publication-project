######################################
### Title: 02_data_analysis
### Author: Shuai Zhu
### Description: analyze publication data
######################################

library(tidyverse)
library(plotly)


### setting working directory
working_directory <-  'C:\\Users\\zhushu\\OneDrive\\Graduate File\\CIDA RA\\publication project'
setwd(working_directory)

### read data

df <- read.csv('./DataRaw/CIDA members publication.csv')


###
df_freq <- df%>%filter(.,pub_year>=2017)%>%
  group_by(pub_year,CIDA.member)%>%
  count()


df_summary <- df_freq%>%
  group_by(pub_year)%>%
  summarise(sum = sum(n),count = n(),mean = mean(n))


## plot

plot_year <- function(year){

  dfi <- filter(df_freq, pub_year==year)%>%arrange(.,desc(n))
  fig <- plot_ly(dfi,
    x = ~CIDA.member,
    y = ~n,
    name = "",
    type = "bar"
  )
  fig%>%layout(title = paste('CIDA members publications by  in', as.character(year)),
               xaxis = list(categoryorder = "total descending", tickangle = 45)
               )
}

plot_year(2018)  

fig <- plot_ly()
fig%>%add_trace(df_freq,)
  
  
  
  
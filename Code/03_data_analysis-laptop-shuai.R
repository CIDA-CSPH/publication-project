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


## plot by years

plot_year <- function(year){

  dfi <- filter(df_freq, pub_year==year)%>%arrange(.,desc(n))
  fig <- plot_ly(dfi,
    x = ~CIDA.member,
    y = ~n,
    name = "",
    type = "bar"
  )
  fig <- fig%>%layout(title = paste('CIDA members publications by individual in', as.character(year)),
               xaxis = list(categoryorder = "total descending", tickangle = 45)
               )

  return(fig)
  
}
## summary table individual

round3 <- function(x) round(x,3)
summary_individual <- function(){
  summarytable <- df_freq%>%
    group_by(CIDA.member)%>%
    summarise(Mean = mean(n),Median = median(n),sd=sd(n),IQR=IQR(n),Num_years=n())%>%
    mutate_if(is.numeric, round3)%>%
    arrange(desc(Mean))

  return(summarytable)
}
summary_table <- summary_individual()

## journal

format_string <- function(string){
  string <- gsub('&','and',string)
  string <- str_to_title(string)
  return(string)
}
journal_table <- sapply(df$journal[df$journal!=""], format_string)%>%table()%>%as.data.frame()%>%
  arrange(desc(Freq))
colnames(journal_table) <- c('Journal title','Num_publications')
summary_journal <- journal_table%>%
  summarise(Num_journals=n(), Mean=mean(Num_publications),Max=max(Num_publications))

  
  
  
  
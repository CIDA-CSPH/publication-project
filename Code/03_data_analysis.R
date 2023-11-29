######################################
### Title: 02_data_analysis
### Author: Shuai Zhu
### Description: analyze publication data
######################################

library(tidyverse)
library(plotly)
library(readxl)

### setting working directory
working_directory <-  'C:\\Users\\zhushu\\OneDrive\\Graduate File\\CIDA RA\\publication project'
setwd(working_directory)

### read data

df <- read.csv('./DataRaw/CIDA members publication.csv')
df <-  df[,c( "CIDA.member" ,"pub_year" )]
df_member <-  read_excel('./DataProcessed/PERSONEL ROSTER for CIDA and B&I-NEC.xlsx')
df_member$CIDA.member <- paste(df_member$`First Name` , df_member$`Last Name`)
df <- merge(df, df_member[,c('CIDA.member', 'Job Title')],by = 'CIDA.member',all.x = T)

###


df[grepl('Professor',df$`Job Title`),"Job Title"] <- 'Professor'

df_freq <- df%>%filter(.,pub_year>=2017)%>%
  group_by(pub_year,CIDA.member,`Job Title`)%>%
  count()

df_summary <- df_freq%>%
  group_by(pub_year)%>%
  summarise(sum = sum(n),count = n(),mean = mean(n))


## plot by years

plot_year <- function(year){

  df_year <- filter(df_freq, pub_year==year)
  ## professors
  fig1 <- plot_ly(x =filter(df_year, `Job Title`=='Professor')$n, type = "histogram")
  ## Research Associate
  fig2 <- plot_ly(x =filter(df_year, `Job Title`=='Research Associate')$n, type = "histogram")
  fig <- subplot(fig1, fig2) %>% layout(title = paste('in', year))
  
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

  
  
  
  
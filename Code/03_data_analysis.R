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

df <- read_excel('./DataRaw/CIDA members google publication.xlsx')
df_copy <- df
df <-  df[,c( "CIDA_member" ,"pub_year" )]
df_member <-  read_excel('./DataProcessed/PERSONEL ROSTER for CIDA and B&I-NEC.xlsx')
df_member$CIDA.member <- paste(df_member$`First Name` , df_member$`Last Name`)
df <- merge(df, df_member[,c('CIDA.member', 'Job Title')],by.x = 'CIDA_member', by.y ='CIDA.member',all.x = T)

###


df[grepl('Professor',df$`Job Title`),"Job Title"] <- 'Professor'

df_freq <- df%>%filter(.,pub_year>=2017)%>%
  group_by(pub_year,CIDA_member,`Job Title`)%>%
  count()

df_summary <- df_freq%>%
  group_by(pub_year)%>%
  summarise(sum = sum(n),count = n(),mean = mean(n))


## plot by years

plot_year <- function(year){

  df_year <- filter(df_freq, pub_year==year)
  ## professors
  fig1 <- plot_ly(x =filter(df_year, `Job Title`=='Professor')$n, 
                  type = "histogram", nbinsx = 10, name ='Professors' )%>%
    layout(bargap= 0.1)
  ## Research Instructor
  fig2 <- plot_ly(x =filter(df_year, `Job Title`=='Research Instructor')$n, 
                  type = "histogram", nbinsx = 10, name = 'Research Instructor')%>%
    layout(bargap= 0.1)
  ## Research Associate
  fig3 <- plot_ly(x =filter(df_year, `Job Title`=='Research Associate')$n, 
                  type = "histogram", nbinsx = 10, name = 'Research Associate')%>%
    layout(bargap= 0.1)
  ## Research Assistant
  fig4 <- plot_ly(x =filter(df_year, `Job Title`=='Research Assistant')$n, 
                  type = "histogram", nbinsx = 10, name = 'Research Assistant')%>%
    layout(bargap= 0.1)
  
  
  fig <- subplot(fig1, fig2, fig3,fig4, nrows =2) %>% layout(title = paste('Distribution of publications in ', year))
  
  return(fig)
}
## summary_table each year

year_table <- df_freq%>%group_by(pub_year)%>%
  summarise(mean = mean(n),num_publication = sum(n),num_members = n())


## c individual

round3 <- function(x) round(x,3)
summary_individual <- function(){
  summarytable <- df_freq%>%
    group_by(CIDA_member)%>%
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



journal_table <- sapply(df_copy$journal[df_copy$journal!=""], format_string)%>%table()%>%as.data.frame()%>%
  arrange(desc(Freq))

colnames(journal_table) <- c('Journal title','Num_publications')
summary_journal <- journal_table%>%
  summarise(Num_journals=n(), Mean=mean(Num_publications),Max=max(Num_publications))

  
  
  
  
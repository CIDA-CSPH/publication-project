######################################
### Title: 02_data_analysis
### Author: Shuai Zhu
### Description: analyze publication data
######################################

library(tidyverse)
library(openxlsx)
### setting working directory
working_directory <-  'P:\\BERD\\publication-project'
setwd(working_directory)

### read data

df <- read.xlsx('./DataRaw/CIDA members google publication.xlsx')%>%tibble()
df_copy <- df
df <-  df[,c( "CIDA_member" ,"pub_year" )]
df_member <-  read.xlsx('./DataProcessed/PERSONEL ROSTER for CIDA and B&I-NEC.xlsx')%>%tibble()
df_member$CIDA.member <- paste(df_member$`First.Name` , df_member$`Last.Name`)
df <- merge(df, df_member[,c('CIDA.member', 'Job.Title')],by.x = 'CIDA_member', by.y ='CIDA.member',all.x = T)%>%tibble()

###


df[grepl('Professor',df$`Job.Title`),"Job Title"] <- 'Professor'
df_freq <- df%>%filter(.,pub_year>=2017)%>%
  group_by(pub_year,CIDA_member,`Job.Title`)%>%
  summarise(`count`= n())
df_freq <- df_freq%>%mutate(`Job.Title`= case_when(str_detect(`Job.Title`, 'Instructor|Research Senior Instructor')~'Research Instructor',
                                        str_detect(`Job.Title`, 'Post-Doctoral Fellow')~'Research Associate',
                                        str_detect(`Job.Title`, 'Grad Assistant')~'Research Assistant',
                                        str_detect(`Job.Title`, 'Professor|Director-Faculty')~'Professors',
                                        .default =`Job.Title`)
                 )

df_summary <- df_freq%>%
  group_by(pub_year)%>%
  summarise(sum = sum(`count`),count = n(),mean = mean(`count`))


## plot by years
df_freq%>%filter(!is.na(`Job.Title`)&`Job.Title`!="Sr Professional Research Asst")%>%
  ggplot(aes(x=`count`))+geom_histogram( binwidth=5, fill="#69b3a2", color="#e9ecef", alpha=1)+xlab('# of publications')+
  facet_wrap(vars(pub_year ,`Job.Title` ), nrow=7)+ggtitle('Histogram of publication number per tittle and year')
ggsave( './Figures/Histogram of publication number per tittle and year.png',dpi = 800, width = 8, height = 14, units = "in")

## summary_table each year

year_table <- df_freq%>%group_by(pub_year)%>%
  summarise(mean = mean(count),num_publication = sum(count),num_members = n())


## c individual

round3 <- function(x) round(x,3)
summary_individual <- function(){
  summarytable <- df_freq%>%
    group_by(CIDA_member)%>%
    summarise(Mean = mean(count),Median = median(count),sd=sd(count),IQR=IQR(count),Num_years=n())%>%
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


  
  
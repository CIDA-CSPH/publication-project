######################################
### Title: 04_network graph
### Author: Shuai Zhu
### Description: make network graph of connection of team members
######################################



library(tidyverse)
library(openxlsx)
library(data.table)
library(igraph)


### setting working directory
working_directory <-  'P:\\BERD\\publication-project'
setwd(working_directory)

### read data
df <- read.xlsx('./DataRaw/CIDA members google publication.xlsx')%>%tibble()
df <- df%>%distinct(article_title,.keep_all = T)
### extract team members from author column
df_member <-  read.xlsx('./DataProcessed/PERSONEL ROSTER for CIDA and B&I-NEC.xlsx')%>%tibble()%>%filter(!is.na(author_id))
CIDA.member <- paste(df_member$`First.Name` , df_member$`Last.Name`)
df_author <- df$author%>%str_split(' and ',simplify = T)%>%as_tibble()

## use regex to extract members name
regex_name <- paste0( substr(df_member$`First.Name`,1,1),'.*' , df_member$`Last.Name`)
name_match <- function(name_vector){
  tryCatch({
    name_vector <- name_vector[!is.na(name_vector)&name_vector!=""]
    name_vector_short <- paste(str_split_i(name_vector, ' ',1)%>%substring(.,1,1), lapply(str_split(name_vector, ' '), tail,1))
    ind <- which(outer(regex_name, name_vector, Vectorize(grepl)), arr.ind = T)
    
    res <- name_vector[ind[,2]]
    names(res) <- regex_name[ind[,1]]
    
    return(res)
  },error = function(e){
    return(NA)
  }
  )
}

name_list <- split(df_author,seq(nrow(df_author))) 
author_connection_list <- lapply(name_list,name_match)
vector_matched <- author_connection_list%>%unlist()%>%as.vector()
names(vector_matched) <- lapply(str_split(author_connection_list%>%unlist()%>%names(),'\\.'),tail,2)
vector_for_remove <- c("James R Johnson", "Cristina L Wood", "Lonnie R Johnson", "Max R Johnson")

df_temp <- str_split(vector_matched,' ',simplify = T)%>%as.data.frame()%>%tibble()
lapply(str_split(author_connection_list%>%unlist()%>%names(),'\\.'),tail,1)


make_links <- function(author_list){
  author_vector <- author_list%>%unlist()%>%as.vector()
  if (identical(author_vector, character(0))|length(author_vector)==1){
    return(NULL)
  }else{
    res_df <- as.data.frame(t(combn(author_vector ,2)))%>%tibble()
    colnames(res_df) <- c('srouce', 'target')
    return(res_df)
  }
}

df_obj <- lapply(author_connection_list,make_links)
links <- rbindlist(df_obj, use.names = TRUE , fill=T)%>%tibble()
network <- graph_from_data_frame(d=links, directed=F) 
deg <- degree(network, mode="all")
plot(network, vertex.color=rgb(0.1,0.7,0.8,0.5))



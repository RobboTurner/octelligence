library(dplyr)
library(readxl)
library(tidyr)
library(purrr)
library(glue)

read_function <- function(sheet, filename) {
  
  question <- read_excel(filename, range = "B4", sheet = sheet, col_names = FALSE)
  
  if (grepl("Summary", question[1,1])) {return(NA)}
  
  table <- read_excel(filename, skip = 6, sheet = sheet, col_names = TRUE, col_types = c("text")) %>% 
    drop_na(4) %>% 
    pivot_longer(cols = -c("...2")) %>% 
    drop_na(value) %>% 
    mutate(value = as.numeric(value),
           question = glue(question[1,1], ...2),
           demographic = replace_na(name, "above - %")) %>% 
    select(-c("...2", name)) %>% 
    drop_na(value) %>% 
    filter(value < 1)
    
  
  return(table)
}

filename = "savanta_data/Omni_W184_HomelessAndPolicePR_tables_Private.xlsx"

sheets = excel_sheets(filename)[2:25]

data_list <- map(sheets, read_function, filename = filename)

output <- bind_rows(data_list[!is.na(data_list)])

readr::write_csv(output, file = "polling.csv")

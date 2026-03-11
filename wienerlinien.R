get_wiener_times <- function(stop_id=NULL,stop_alias=NULL, max_window=15) {
  library(httr)
  library(jsonlite)
  library(dplyr)
  
  if(!is.null(stop_alias)){
  stop.ref=list(
   "CBR2prater"=381,
   "CBR2westbhf"=355,
   "home2westbhf"=1561,
   "home2rodaun"=1533,
   "westbhf2CBR"=370,
   "westbhfU6flor"=4619,
   "westbhfU6sieb"=4610,
   "alserU6sieb"=4606,
   "gumpU6flor"=4618,
   "gumpU6sieb"=4611
  )
  stop_id=stop.ref[[stop_alias]]
  }
  # Wiener Linien Monitor API endpoint
  base_url <- "https://www.wienerlinien.at/ogd_realtime/monitor"
  
  # Make request
  
  response <- GET(
    url = base_url,
    query = list(stopId = stop_id)
  )
  
  # Check for errors
  stop_for_status(response)
  
  # Parse JSON
  content_json <- content(response, as = "text", encoding = "UTF-8")
  parsed <- fromJSON(content_json, flatten = TRUE)
  
  # Extract departures
  departures <- parsed$data$monitors$lines 
  
  if (length(departures) == 0) {
    return("No real-time departures found.")
  }else{
  
  # Format output
result=lapply(departures, function(line) line$departures.departure %>% as.data.frame %>% dplyr::mutate(stop_id=!!stop_id, stop_alias=!!stop_alias,line=vehicle.name,dest=vehicle.towards,when=departureTime.timePlanned, countdown=departureTime.countdown) %>% dplyr::select(stop_id, stop_alias, line, dest, when, countdown)) %>% bind_rows %>% dplyr::filter(countdown<max_window)
  }
  
  return(result)
}

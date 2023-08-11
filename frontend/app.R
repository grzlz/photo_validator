library(shiny)
library(httr)
library(base64enc)

# UI
ui <- fluidPage(
  titlePanel("Image Tagging Automation"),
  sidebarLayout(
    sidebarPanel(
      fileInput("image_upload", "Choose images",
                multiple = TRUE, accept = c("image/png", "image/jpeg", "image/gif"))
    ),
    mainPanel(
      imageOutput("image_display"),
      textOutput("image_tags"),
      actionButton("accept_tags", "Accept Tags"),
      actionButton("reject_tags", "Reject Tags")
    )
  )
)

# Server
server <- function(input, output, session) {
  current_image_index <- reactiveVal(1)
  
  tags_for_image <- function(image_path) {
    # Convert the image to base64
    img_data <- file(image_path, "rb")
    img_content <- readBin(img_data, "raw", file.info(image_path)$size)
    base64_img <- base64encode(img_content)
    
    # Send the base64 encoded image to the API using POST
    url <- "https://20fmt24vrj.execute-api.us-west-1.amazonaws.com/prod/getTag"
    response <- POST(url, body = base64_img, encode = "raw", add_headers("Content-Type" = "text/plain"))
    
    # Parse the response
    cuerpo_respuesta <- content(response, "text")
    return(cuerpo_respuesta)
  }
  
  output$image_display <- renderImage({
    if (is.null(input$image_upload)) {
      return(NULL)
    }
    list(src = input$image_upload$datapath[current_image_index()],
         alt = paste("Image", current_image_index()),
         width = "99%",
         height = "90%")
  }, deleteFile = FALSE)
  
  output$image_tags <- renderText({
    if (is.null(input$image_upload)) {
      return(NULL)
    }
    tags_for_image(input$image_upload$datapath[current_image_index()])
  })
  
  observeEvent(c(input$accept_tags, input$reject_tags), {
    if (current_image_index() < length(input$image_upload$datapath)) {
      current_image_index(current_image_index() + 1)
    }
  })
}

# Run the app
shinyApp(ui = ui, server = server)

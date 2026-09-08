
from docling.datamodel.backend_options import HTMLBackendOptions
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    ConvertPipelineOptions,
    PictureDescriptionApiOptions,
)
from docling.document_converter import DocumentConverter, HTMLFormatOption

# Enable image fetching so <img> tags get embedded (local/relative or remote, as needed)  
html_backend_options = HTMLBackendOptions(  
    fetch_images=True,  
    enable_local_fetch=True,   # allow reading local image files referenced by the HTML  
    enable_remote_fetch=True,  # allow fetching remote (http/https) images, if any  
)  
  
pipeline_options = ConvertPipelineOptions(  
    do_picture_description=True,  
)  
  
# Point picture description at a local Ollama server running qwen3-vl:4b  
pipeline_options.enable_remote_services = True  # required for any remote/API-based model call  
pipeline_options.picture_description_options = PictureDescriptionApiOptions(  
    url="http://localhost:11434/v1/chat/completions",  
    params={"model": "qwen3-vl:1.7b"},
    prompt="Describe the image in three sentences. Be concise and accurate.",  
    timeout=300,  
)  
  
converter = DocumentConverter(  
    format_options={  
        InputFormat.HTML: HTMLFormatOption(  
            pipeline_options=pipeline_options,  
            backend_options=html_backend_options,  
        )  
    }  
)  
  
result = converter.convert("Docling_Library.html")  # or a URL  
doc = result.document  
  
markdown = doc.export_to_markdown()  
with open("output.md", "w", encoding="utf-8") as f:  
    f.write(markdown)
from distro250ls import encode, decode
from PIL import Image
import gradio as gr
import ast, io, base64

def encodeUI(chipertext:str):
    return encode(chipertext)

def decodeUI(encodedText:str):
    encodedList = ast.literal_eval(encodedText)
    return decode(encodedList)

def encodeImage(image:Image.Image, width=300, height=300):
    image.thumbnail((width, height), Image.LANCZOS)
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    encoded_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")
    return encode(encoded_image)

def decodeImage(encodedImageText:str):
    encodedImageList = ast.literal_eval(encodedImageText)
    decodedImageText = decode(encodedImageList)
    decoded_image_data = base64.b64decode(decodedImageText)
    image = Image.open(io.BytesIO(decoded_image_data))
    return image

callback = gr.CSVLogger()

with gr.Blocks(title="Distro25o") as demo:
    inputEnc = gr.Textbox(label="Chipertext")
    outputEnc = gr.Textbox(label="Encoded Text")
    encodeButton = gr.Button("Encode")
    encodeButton.click(encodeUI, inputs=inputEnc, outputs=outputEnc)

    inputDec = gr.Textbox(label="Encoded Text")
    outputDec = gr.Textbox(label="Chipertext")
    decodeButton = gr.Button("Decode")
    decodeButton.click(decodeUI, inputs=inputDec, outputs=outputDec)

    imageSizeW = gr.Number(label="Image Width")
    imageSizeH = gr.Number(label="Image Height")

    imgInputEnc = gr.Image(type="pil", label="Input Image")
    imgOutputEnc = gr.Textbox(label="Encoded Image")
    imgEncodeButton = gr.Button("Encode Image")
    imgEncodeButton.click(encodeImage, inputs=[imgInputEnc, imageSizeW, imageSizeH], outputs=imgOutputEnc)

    imgInputDec = gr.Textbox(label="Encoded Image")
    imgOutputDec = gr.Image(type="pil", label="Decoded Image")
    imgEncodeButton = gr.Button("Decode Image")
    imgEncodeButton.click(decodeImage, inputs=imgInputDec, outputs=imgOutputDec)

    btnSaveData = gr.Button("Save Data")

    callback.setup([inputEnc, outputEnc, inputDec, outputDec, imageSizeW, imageSizeH, imgInputEnc, imgOutputEnc, imgInputDec, imgOutputDec], "flagged_data_points")
    btnSaveData.click(lambda *args: callback.flag(args), [inputEnc, outputEnc, inputDec, outputDec, imageSizeW, imageSizeH, imgInputEnc, imgOutputEnc, imgInputDec, imgOutputDec], None, preprocess=False)

demo.launch()
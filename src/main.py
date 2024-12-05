from libs.distro250ls import encode, decode
import argparse, contextlib, webbrowser, base64, io, ast, msvcrt, qrcode, datetime
from PIL import Image
import gradio as gr

def encodeUI(chipertext: str):
    return encode(chipertext)


def decodeUI(encodedText: str):
    encodedList = ast.literal_eval(encodedText)
    return decode(encodedList)


def encodeImage(image: Image.Image, width=300, height=300):
    currDatetime = datetime.datetime.now()

    image.thumbnail((width, height), Image.Resampling.NEAREST)
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    encoded_image = base64.b64encode(img_bytes.getvalue()).decode("utf-8")

    try:
        f = open(f"saved_files/encodedImage-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "x", encoding="utf-8")
    except:
        f = open(f"saved_files/encodedImage-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w", encoding="utf-8")

    f.write(str(encode(encoded_image)))
    f.close()

def decodeImageSave(file):
    currDatetime = datetime.datetime.now()

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    encodedImageList = ast.literal_eval(content)
    decodedImageText = decode(encodedImageList)
    decoded_image_data = base64.b64decode(decodedImageText)
    image = Image.open(io.BytesIO(decoded_image_data))

    image.save(f"saved_files/decodedImage-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.png")

def decodeImage(file):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    encodedImageList = ast.literal_eval(content)
    decodedImageText = decode(encodedImageList)
    decoded_image_data = base64.b64decode(decodedImageText)
    image = Image.open(io.BytesIO(decoded_image_data))

    return image


def generateQRcode(link):
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = "qr_code.png"
    img.save(img_path)
    return img_path


def encFile(file):
    currDatetime = datetime.datetime.now()

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        f = open(f"saved_files/encodedFile-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "x", encoding="utf-8")
    except:
        f = open(f"saved_files/encodedFile-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w", encoding="utf-8")

    f.write(str(encode(content)))
    f.close()

def decFileSave(file):
    currDatetime = datetime.datetime.now()

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        f = open(f"saved_files/decodedFile-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "x", encoding="utf-8")
    except:
        f = open(f"saved_files/decodedFile-{currDatetime.strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w", encoding="utf-8")

    f.write(decode(ast.literal_eval(content)))
    f.close()

def decFile(file):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    return decode(ast.literal_eval(content))


def encAudio(fileP):
    with open(fileP, "rb") as f:
        contents = f.read()

    return encode(str(contents))


def decAudio(encAudioText):
    encAudioList = ast.literal_eval(encAudioText)
    decAudioText = decode(encAudioList)
    return decAudioText


def encVideo(video):
    with open(video, "rb") as f:
        contents = f.read()

    return encode(str(contents))


def decVideo(encVideoText):
    encVideoList = ast.literal_eval(encVideoText)
    decAudioText = decode(encVideoList)
    return decAudioText


margin = """<div style="margin-top: 150px;"></div>"""
callback = gr.CSVLogger()

with gr.Blocks(title="Distro50") as demo:
    inputEnc = gr.Textbox(label="Chipertext")
    outputEnc = gr.Textbox(label="Encoded Text")
    encodeButton = gr.Button("Encode Text")
    encodeButton.click(encodeUI, inputs=inputEnc, outputs=outputEnc)

    gr.Markdown(margin)

    inputDec = gr.Textbox(label="Encoded Text")
    outputDec = gr.Textbox(label="Chipertext")
    decodeButton = gr.Button("Decode Text")
    decodeButton.click(decodeUI, inputs=inputDec, outputs=outputDec)

    gr.Markdown(margin)

    inputFileEnc = gr.UploadButton(label="Upload File", type="filepath")
    fileEncButton = gr.Button("Encode File")
    fileEncButton.click(fn=encFile, inputs=inputFileEnc)

    gr.Markdown(margin)

    inputFileDec = gr.UploadButton(label="Upload Encoded File", type="filepath")
    fileDecButton = gr.Button("Decode File")
    fileDecButtonSave = gr.Button("Save Decoded File")
    outputFileDec = gr.Textbox(label="Chiper File")
    fileDecButton.click(fn=decFile, inputs=inputFileDec, outputs=outputFileDec)
    fileDecButtonSave.click(fn=decFileSave, inputs=inputFileDec)
    
    gr.Markdown(margin)

    audioInputEnc = gr.Audio(label="Upload Audio", type="filepath")
    audioOutputEnc = gr.Textbox(label="Encoded File")
    audioEncButton = gr.Button("Encode Audio")
    audioEncButton.click(fn=encAudio, inputs=audioInputEnc, outputs=audioOutputEnc)

    gr.Markdown(margin)

    audioInputDec = gr.Textbox(label="Encoded Audio")
    audioOutputDec = gr.Audio(label="Decoded Audio")
    audioDecButton = gr.Button("Decode Audio")
    audioDecButton.click(fn=decAudio, inputs=audioInputDec, outputs=audioOutputDec)

    gr.Markdown(margin)

    imageSizeW = gr.Number(label="Image Width")
    imageSizeH = gr.Number(label="Image Height")

    imgInputEnc = gr.Image(type="pil", label="Input Image")
    imgEncodeButton = gr.Button("Encode Image")
    imgEncodeButton.click(
        encodeImage, inputs=[imgInputEnc, imageSizeW, imageSizeH]
    )

    gr.Markdown(margin)

    imgInputDec = gr.UploadButton(label="Upload Encoded Image", type="filepath")
    imgEncodeButton = gr.Button("Decode Image")
    imgOutputDec = gr.Image(type="pil", label="Decoded Image")
    imgEncodeButtonSave = gr.Button("Save Decoded Image")
    imgEncodeButton.click(decodeImage, inputs=imgInputDec, outputs=imgOutputDec)
    imgEncodeButtonSave.click(decodeImageSave, inputs=imgInputDec)

    gr.Markdown(margin)

    videoInputEnc = gr.Video(label="Input Video")
    videoOutputEnc = gr.Textbox(label="Encoded Video")
    videoEncodeButton = gr.Button("Encode Video")
    videoEncodeButton.click(encVideo, inputs=videoInputEnc, outputs=videoOutputEnc)

    gr.Markdown(margin)

    videoInputDec = gr.Textbox(label="Encoded Video")
    videoOutputDec = gr.Video(label="Decoded Video")
    videoDecodeButton = gr.Button("Decode Video")
    videoDecodeButton.click(decVideo, inputs=videoInputDec, outputs=videoOutputDec)

    btnSaveData = gr.Button("Save Data")

    callback.setup(
        [
            inputEnc,
            outputEnc,
            inputDec,
            outputDec,
            imageSizeW,
            imageSizeH,
            imgInputEnc,
            imgInputDec,
            imgOutputDec,
        ],
        "flagged_data_points",
    )
    btnSaveData.click(
        lambda *args: callback.flag(args),
        [
            inputEnc,
            outputEnc,
            inputDec,
            outputDec,
            imageSizeW,
            imageSizeH,
            imgInputEnc,
            imgInputDec,
            imgOutputDec,
        ],
        None,
        preprocess=False,
    )

    # QRLink = "https://github.com/Hipex123"
    # qrImage = gr.Image(generateQRcode(QRLink))

    gr.Markdown(
        """
            <div style="text-align: right; margin-top: 20px;">
                <a href="https://github.com/Hipex123" target="_blank" style="font-size: 25px; color: white;">
                    View on GitHub
                </a>
            </div>
        """
    )

parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--share",
    action="store_true",
    help="share your web server with a public domain (must be used with -r flag)",
)
parser.add_argument(
    "-r",
    "--run",
    action="store_true",
    help="start a web server",
)

args = parser.parse_args()
buffer = io.StringIO()

if args.run and args.share:
    with contextlib.redirect_stdout(buffer):
        demo.launch(share=True, prevent_thread_lock=True)

    output = buffer.getvalue()
    print(output)
    for line in output.splitlines():
        if "Running on public URL:" in line:
            publicUrl = line[23:]

    webbrowser.open(publicUrl)
    print("Press any key to shutdown server...")
    msvcrt.getch()

elif args.run and not args.share:
    demo.launch(prevent_thread_lock=True)
    webbrowser.open("http://127.0.0.1:7860/")
    print("Press any key to shutdown server...")
    msvcrt.getch()
    
elif args.share and not args.run:
    print("No run flag specified.")
    print("Quitting...")
    exit(1)

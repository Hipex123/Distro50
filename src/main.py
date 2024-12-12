from libs.distro250ls import encode, decode
import argparse, contextlib, webbrowser, base64, io, ast, msvcrt, qrcode, datetime, time, tempfile, os
from PIL import Image
import gradio as gr

tempHolder: str = ""

def removeTempFile():
    if tempHolder != "":
        try:
            os.remove(tempHolder)
            print("------------------")
            print(f"Deleted temp file: {tempHolder}")
        except OSError as e:
            print("------------------")
            print(f"Error deleting temp file: {e}")

def createTempEncFile(buffer):
    global tempHolder

    removeTempFile()

    tempFile = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    tempFile.write(str(encode(buffer)).encode("utf-8"))
    tempFile.close()


    tempHolder = tempFile.name
    return tempHolder

def createTempDecFile(buffer, suffixP: str, special: any = 0):
    global tempHolder

    removeTempFile()

    tempFile = tempfile.NamedTemporaryFile(delete=False, suffix=suffixP)
    tempFile.write(buffer)
    tempFile.close()

    tempHolder = tempFile.name

    if special == 0:
        return tempHolder, tempHolder
    else:
        return special, tempHolder


def encodeUI(plaintext):
    return encode(plaintext)

def decodeUI(ciphertext):
    encodedList = ast.literal_eval(ciphertext)
    return decode(encodedList)


def encodeImage(image: Image.Image, width=300, height=300):
    image.thumbnail((width, height), Image.Resampling.NEAREST)

    imageBytes = io.BytesIO()
    image.save(imageBytes, format="PNG")
    encodedImage = base64.b64encode(imageBytes.getvalue()).decode("utf-8")

    return createTempEncFile(encodedImage)

def decodeImage(file):
    global tempHolder

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    encodedImageList = ast.literal_eval(content)
    decodedImageText = decode(encodedImageList)
    decoded_image_data = base64.b64decode(decodedImageText)
    image = Image.open(io.BytesIO(decoded_image_data))

    removeTempFile()
    tempFile = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    image.save(tempFile, format="PNG")
    tempFile.close()

    tempHolder = tempFile.name
    return image, tempHolder


def generateQRcode(link):
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_path = "qr_code.png"
    img.save(img_path)
    return img_path


def encFile(plainFile):
    with open(plainFile, "r", encoding="utf-8") as f:
        content = f.read()

    return createTempEncFile(content)

def decFile(cipherFile):
    with open(cipherFile, "r", encoding="utf-8") as f:
        content = f.read()
    plainFile = decode(ast.literal_eval(content))

    return createTempDecFile(plainFile.encode("utf-8"), ".txt", plainFile)


def encAudio(plainFile):
    with open(plainFile, "rb") as f:
        content = f.read()

    encodedContent = base64.b64encode(content).decode("utf-8")

    return createTempEncFile(encodedContent)

def decAudio(chiperFile):
    with open(chiperFile, "r", encoding="utf-8") as f:
        contents = ast.literal_eval(f.read())

    decodedContent = decode(contents)
    decodedContentBin = base64.b64decode(decodedContent)

    return createTempDecFile(decodedContentBin, ".mp3")


def encVideo(plainVideo):
    with open(plainVideo, "rb") as f:
        content = f.read()
    
    contentStr = base64.b64encode(content).decode("utf-8")

    return createTempEncFile(contentStr)

def decVideo(cipherVideo):
    with open(cipherVideo, "r", encoding="utf-8") as f:
        content = ast.literal_eval(f.read())
    
    decodedContent = decode(content)
    decodedContentBin = base64.b64decode(decodedContent)

    return createTempDecFile(decodedContentBin, ".mp4")

def openPublicUrl():
    with contextlib.redirect_stdout(buffer):
        demo.launch(share=True, prevent_thread_lock=True)

    output = buffer.getvalue()
    print(output)
    for line in output.splitlines():
        if "Running on public URL:" in line:
            linkIndex = line.find("https://")
            publicUrl = line[linkIndex:]
            print(line)

    webbrowser.open(publicUrl)
    print("Press any key to shutdown server...")
    msvcrt.getch()

def openLocalUrl():
    demo.launch(prevent_thread_lock=True)
    webbrowser.open("http://127.0.0.1:7860/")
    print("Press any key to shutdown server...")
    msvcrt.getch()

margin = """<div style="margin-top: 150px;"></div>"""
callback = gr.CSVLogger()

with gr.Blocks(title="Distro50") as demo:
    # TEXT

    gr.Markdown(
        """
            <h1>Text</h1>
            <div style="height:2px; background: gray;"/>
        """
    )

    inputEnc = gr.Textbox(label="Plaintext")
    outputEnc = gr.Textbox(label="Ciphertext")
    encodeButton = gr.Button("Encode Text")
    encodeButton.click(encodeUI, inputs=inputEnc, outputs=outputEnc)

    gr.Markdown(margin)

    inputDec = gr.Textbox(label="Ciphertext")
    outputDec = gr.Textbox(label="Plaintext")
    decodeButton = gr.Button("Decode Text")
    decodeButton.click(decodeUI, inputs=inputDec, outputs=outputDec)

    gr.Markdown(margin)

    # FILES

    gr.Markdown(
        """
            <h1>Files</h1>
            <div style="height:2px; background: gray;"/>
        """
    )

    inputFileEnc = gr.UploadButton(label="Upload Plain File", type="filepath")
    fileEncButton = gr.Button("Encode File")
    fileEncButton.click(fn=encFile, inputs=inputFileEnc, outputs=gr.File())

    gr.Markdown(margin)

    inputFileDec = gr.UploadButton(label="Upload Cipher File", type="filepath")
    fileDecButton = gr.Button("Decode File")
    outputFileDec = gr.Textbox(label="Plain File")
    fileDecButton.click(fn=decFile, inputs=inputFileDec, outputs=[outputFileDec, gr.File()])
    
    gr.Markdown(margin)

    # AUDIO

    gr.Markdown(
        """
            <h1>Audio</h1>
            <div style="height:2px; background: gray;"/>
        """
    )

    audioInputEnc = gr.Audio(label="Upload Plain Audio", type="filepath")
    audioEncButton = gr.Button("Encode Audio")
    audioEncButton.click(fn=encAudio, inputs=audioInputEnc, outputs=gr.File())

    gr.Markdown(margin)

    audioInputDec = gr.UploadButton(label="Upload Cipher Audio", type="filepath")
    audioDecButton = gr.Button("Decode Audio")
    audioOutputDec = gr.Audio(label="Plain Audio")
    audioDecButton.click(fn=decAudio, inputs=audioInputDec, outputs=[audioOutputDec, gr.File()])

    gr.Markdown(margin)

    # IMAGES

    gr.Markdown(
        """
            <h1>Images</h1>
            <div style="height:2px; background: gray;"/>
        """
    )

    imageSizeW = gr.Number(label="Image Width")
    imageSizeH = gr.Number(label="Image Height")

    imgInputEnc = gr.Image(type="pil", label="Plain Image")
    imgEncodeButton = gr.Button("Encode Image")
    imgEncodeButton.click(
        encodeImage, inputs=[imgInputEnc, imageSizeW, imageSizeH], outputs=gr.File()
    )

    gr.Markdown(margin)

    imgInputDec = gr.UploadButton(label="Upload Cipher Image", type="filepath")
    imgDecodeButton = gr.Button("Decode Image")
    imgOutputDec = gr.Image(type="pil", label="Plain Image")
    imgDecodeButton.click(decodeImage, inputs=imgInputDec, outputs=[imgOutputDec, gr.File()])

    gr.Markdown(margin)

    # VIDEO

    gr.Markdown(
        """
            <h1>Video</h1>
            <div style="height:2px; background: gray;"/>
        """
    )

    videoInputEnc = gr.Video(label="Plain Video")
    videoEncodeButton = gr.Button("Encode Video")
    videoEncodeButton.click(encVideo, inputs=videoInputEnc, outputs=gr.File())

    gr.Markdown(margin)

    videoInputDec = gr.UploadButton(label="Cipher Video", type="filepath")
    videoDecodeButton = gr.Button("Decode Video")
    videoOutputDec = gr.Video(label="Plain Video")
    videoDecodeButton.click(decVideo, inputs=videoInputDec, outputs=[videoOutputDec, gr.File()])

    gr.Markdown(margin)

    btnSaveData = gr.Button("Save Data To The Server")

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
        "../flagged_data_points",
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
    openPublicUrl()

elif args.run and not args.share:
    openLocalUrl()
    
elif args.share and not args.run:
    openPublicUrl()
